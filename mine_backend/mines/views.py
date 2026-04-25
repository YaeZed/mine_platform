import traceback

from django.db import transaction
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Mine, ThreeDMineTunnel, Tunnel
from .serializers import MineSerializer, ThreeDMineTunnelSerializer
from .algorithm import vno


class MinesList(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request):
        # 从请求头中获取自定义用户名
        username = request.headers.get('x-username')
        # 根据用户名过滤矿井数据
        mines = Mine.objects.filter(mine_username=username)

        # 如果没有找到任何矿井，返回 404
        if not mines.exists():
            return Response({"error": "未找到相关的矿井信息"}, status=status.HTTP_404_NOT_FOUND)

        serializer = MineSerializer(mines, many=True)
        data = {
            'status': 200,
            'message': '获取成功',
            'data': serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        # 获取请求体中的矿井数据
        mine_data = request.data
        # 创建矿井实例
        mine = Mine()
        # 给实例设置数据
        mine_username = mine_data.get('mine_username')
        mine_name = mine_data.get('mine_name')
        mine_desc = mine_data.get('mine_desc')
        # 保存实例到数据库
        try:
            mine = Mine.objects.create(mine_username=mine_username, mine_name=mine_name, mine_desc=mine_desc)
        except Exception as e:
            return Response({
                'status': 400,
                'message': '创建失败',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

        # 序列化返回
        serializer = MineSerializer(mine)
        data = {
            'status': 201,
            'message': '创建成功',
            'data': serializer.data
        }
        return Response(data, status=status.HTTP_201_CREATED)


class MinesDetail(APIView):
    def post(self, request, pk):
        # 从请求中获取mine_id
        mine = Mine.objects.get(mine_id=pk)
        # 获取请求体中的矿井数据
        mine_data = request.data
        # 更新矿井实例
        mine_name = mine_data.get('mine_name')
        mine_desc = mine_data.get('mine_desc')
        # 保存实例到数据库
        try:
            mine.mine_name = mine_name
            mine.mine_desc = mine_desc
            mine.save()
        except Exception as e:
            return Response({
                'status': 400,
                'message': '更新失败',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        # 序列化返回
        serializer = MineSerializer(mine)
        data = {
            'status': 200,
            'message': '更新成功',
            'data': serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        # 从请求中获取mine_id
        mine = Mine.objects.get(mine_id=pk)
        # 删除矿井实例
        try:
            mine.delete()
        except Exception as e:
            return Response({
                'status': 400,
                'message': '删除失败',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        # 序列化返回
        data = {
            'status': 204,
            'message': '删除成功'
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)


class ThreeDMineTunnelData(APIView):
    tubes = ThreeDMineTunnel()

    def get(self, request):
        # get请求，返回所有的3D矿井隧道数据
        tubes = ThreeDMineTunnel.objects.all()
        serializer = ThreeDMineTunnelSerializer(tubes, many=True)
        data = {
            'status': 200,
            'message': '获取成功',
            'data': serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        pass


class RunVentilationSimulation(APIView):
    """
    一个用于执行通风算法并更新数据库的API视图。

    接受POST请求，从数据库中读取隧道数据，执行 vno.py 中的算法，
    并将计算出的风量(q)和阻力(h)写回数据库。
    """

    def post(self, request, *args, **kwargs):
        """
        处理POST请求，执行算法并返回结果。
        """
        try:
            # 1. 从数据库中读取所有隧道数据
            tunnels_queryset = Tunnel.objects.all()

            if not tunnels_queryset.exists():
                return Response(
                    {'status': 'error', 'message': '数据库中没有隧道数据，请先添加。'},
                    status=status.HTTP_404_NOT_FOUND
                )

            # 2. 准备算法所需的输入数据
            # 这里的数据格式必须与 vno.py 中的 build_network 函数所期望的格式完全匹配。
            graph_data_edges = []
            for tunnel in tunnels_queryset:
                # 使用 tunnel_id 作为算法中的 id 字段，以及 start_id 和 end_id
                graph_data_edges.append({
                    "id": tunnel.tunnel_id,
                    "r": tunnel.r,
                    "s": tunnel.start_id,
                    "t": tunnel.end_id,
                })

            # 这里的 fans, qFixs, gates 等字段根据你的实际算法需求设置。
            graph_data_fans = [
                {"a0": 1046.3, "a1": 5.0, "a2": -0.85, "eID": 34},
                {"a0": 1046.3, "a1": 5.0, "a2": -0.85, "eID": 14}
            ]
            # 示例中，我们假设这些数据来自数据库，但在这里是空的列表。
            graph_datas = {
                "edges": graph_data_edges,
                "fans": graph_data_fans,
                "maxCount": 1000,
                "precise": 0.0001
            }

            # 3. 构造通风网络并执行算法
            vent_network = vno.VentNetwork()
            if not vno.build_network(graph_datas, vent_network.graph()):
                return Response(
                    {'status': 'error', 'message': '构造通风网络失败，请检查数据完整性。'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            vent_network.addVirtualST()
            simulation_success = vno.vno(vent_network)
            vent_network.delVirtualST()

            if not simulation_success:
                return Response(
                    {'status': 'error', 'message': '算法解算失败，未收敛。请检查输入数据。'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 4. 将算法的输出写回数据库
            # 使用数据库事务确保所有更新要么全部成功，要么全部回滚，防止数据不一致。
            with transaction.atomic():
                for edge in vent_network.graph().es:
                    try:
                        # 使用 tunnel_id 进行查询，而不是默认的 id
                        tunnel = tunnels_queryset.get(tunnel_id=edge['id'])

                        # 更新风量和阻力字段
                        tunnel.q = edge['q']
                        tunnel.h = vno.f0(edge)
                        tunnel.save()

                    except Tunnel.DoesNotExist:
                        # 如果算法中存在数据库没有的边，则跳过
                        continue

            return Response({
                'status': 'success',
                'message': '风量和阻力已成功更新到数据库。'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            # 捕获所有异常并返回详细信息，这对于调试至关重要
            traceback.print_exc()
            return Response(
                {'status': 'error', 'message': f'发生未知错误：{str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
