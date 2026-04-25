import re


from rest_framework.views import APIView


from users.models import User
from .serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework.response import Response
from rest_framework import status

class LoginView(TokenObtainPairView):
    # 登录视图
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        # 自定义登录成功后返回的结果
        result = serializer.validated_data
        user = serializer.user # 获取user对象，方便后续使用

        data = {
            'id': user.id,
            'mobile': user.mobile,
            'username': user.username,
            'email': user.email,
            'token': result.pop('access'),  # 将 access 替换为 token
            'nickname':user.nickname,
        }

        response_data = {
            'status': 200,
            'data': data,
        }

        return Response(response_data, status=status.HTTP_200_OK)



class RegisterView(APIView):
    # 注册视图
    def post(self, request):
        # 一 获取参数
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        password_confirm = request.data.get('password_confirm')

        # 二 校验参数
        # 2.1 参数完整性校验
        if not all([username, password, email, password_confirm]):
            return Response({'message': '参数不完整'}, status=status.HTTP_400_BAD_REQUEST)
        # 2.2 名称重复校验
        if User.objects.filter(username=username).exists():
            return Response({'message': '用户名已存在'}, status=status.HTTP_400_BAD_REQUEST)
        # 2.3 密码校验
        if password != password_confirm:
            return Response({'message': '两次密码不一致'}, status=status.HTTP_400_BAD_REQUEST)
        # 2.4 密码长度校验
        if not (6 <= len(password) <= 18):
            return Response({'message': '密码长度须在6-18位之间'}, status=status.HTTP_400_BAD_REQUEST)
        # 2.5 邮箱重复校验
        if User.objects.filter(email=email).exists():
            return Response({'message': '邮箱已被注册'}, status=status.HTTP_400_BAD_REQUEST)
        # 2.6 邮箱格式校验
        if not re.match(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', email):
            return Response({'message': '邮箱格式不正确'}, status=status.HTTP_400_BAD_REQUEST)

        # 三 保存用户信息
        user = User.objects.create_user(username=username, password=password, email=email)
        res = {
            'username': user.username,
            'email': user.email,
            'id': user.id,
        }
        return Response(res, status=status.HTTP_201_CREATED)

class EditView(APIView):
    def post(self, request, pk):
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response({"message": "用户不存在"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user, data=request.data, partial=True)  # 重要: 添加 partial=True
        if serializer.is_valid():
            serializer.save()
            return Response({"status": 200, "data": serializer.data, "message": "更新成功"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)