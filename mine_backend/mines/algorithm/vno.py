# -*- coding: utf-8 -*-
#-*- coding:utf-8 -*-
import time
import os
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
#import networkx as nx
from igraph import *
# import pygraphviz as pgv
from queue import PriorityQueue
print ('你好啊')
#表示无穷大
DBL_MAX = 1.0e6
#放大因子
LARGE_COEFF = 1e3

#增加虚拟源点以及虚拟的出边
def add_virtual_source(dg):
	#查找所有入度等于0的节点
	nodes = dg.vs.select(_indegree=0)
	if len(nodes) == 0:return -1
	#增加一个虚拟源点
	dg.add_vertex()
	sn = dg.vs.indices[-1]
	#增加虚拟分支(虚拟源点-->)
	for u in nodes:
		dg.add_edge(sn, u.index)
	#返回新增的虚拟源点
	return sn

#增加虚拟汇点以及虚拟的入边
def add_virtual_target(dg):
	#查找所有出度等于0的节点
	nodes = dg.vs.select(_outdegree=0)
	if len(nodes) == 0:return -1
	#增加一个虚拟汇点
	dg.add_vertex()
	tn = dg.vs.indices[-1]
	#增加虚拟分支(-->虚拟汇点)
	for u in nodes:
		dg.add_edge(u.index, tn)
	#返回新增的虚拟汇点
	return tn
def h0(e):
	q, a0, a1, a2 = e['q'],e['a0'],e['a1'],e['a2']

	return np.polyval([a2, a1, a0], q)
def h1(e):
	q, a0, a1, a2 = e['q'],e['a0'],e['a1'],e['a2']
	return np.polyval([2*a2, a1], q)

#e是一个igraph.Edge类型变量
#分支的摩擦鞥组
def R0(e):
	return e['r']

#e是一个igraph.Edge类型变量
#分支的总风阻(包括调节风阻)
def R(e):
	return e['r']+e['adjust_r']

#e是一个igraph.Edge类型变量
#分支的调节风阻(通过调节压力，也就是压差来计算)
def dR(e):
	return 0.0 if abs(e['q']) < 1e-4 else e['adjust_h']/e['q']

#e是一个igraph.Edge类型变量
#分支的阻力h=r*q^2
def f0(e):
	return R(e)*e['q']*abs(e['q'])

#e是一个igraph.Edge类型变量
#分支阻力的1阶导
def f1(e):
	return 2*abs(e['q']*R(e))

#e是一个igraph.Edge类型变量
#是否虚拟分支
def is_zero_edge(e):
	return abs(e['r']) < 1e-4

#e是一个igraph.Edge类型变量
#是否固定风量分支
def is_fix_edge(e):
	return abs(e['fq']) > 0

#e是一个igraph.Edge类型变量
#是否风机分支(分支上有风机)
def is_fan_edge(e):
	return not (e['a0']==0 and e['a1']==0 and e['a2']==0)

#创建图的拓扑关系(节点和分支,以及实际id与igraph内部编号之间的映射)
def build_graph(edges, dg):
	#收集所有的节点
	sIDs = [data['s'] for data in edges]
	tIDs = [data['t'] for data in edges]
	sIDs.extend(tIDs);
	#构造节点集合(利用set去除重复编号,并排序,然后再转换成list)
	nIDs = set(sIDs)
	#构造节点编号到igraph内部编号的映射关系
	nodes_map = dict(zip(nIDs, range(len(nIDs))));
	#有向图增加节点(igraph节点内部编号从0开始)
	dg.add_vertices(len(nodes_map))
		
	#构造分支编号到igraph内部编号的映射关系
	edges_map = {}
	for i, data in enumerate(edges):
		eID, u, v, r = data['id'], data['s'], data['t'], data['r']
		u, v = nodes_map[u], nodes_map[v] #转换成igraph内部的编号
		edges_map[eID] = i #记录分支编号到igraph内部编号的映射关系
		dg.add_edge(u, v)  #增加新分支(igraph分支内部编号从0开始)
	return nodes_map, edges_map

def set_graph_ids(dg, nodes_map, edges_map):
	#设置igraph节点的id属性数据
	for u in nodes_map:
		i = nodes_map[u]
		dg.vs[i]['id'] = u
	#设置igraph分支的id属性数据
	for e in edges_map:
		i = edges_map[e]
		dg.es[i]['id'] = e

#初始化图的属性默认值
def init_graph_property(dg):
	dg.es['id']=0
	dg.es['a0']=0.0
	dg.es['a1']=0.0
	dg.es['a2']=0.0
	dg.es['r']=0.0
	dg.es['q']=0.0
	dg.es['fq']=0.0
	dg.es['adjust_r']=0.0
	dg.es['adjust_h']=0.0
	dg.es['density']=1.2
	#节点数据
	dg.vs['id']=0
	dg.vs['p']=0.0
	dg.vs['x']=0.0
	dg.vs['y']=0.0
	dg.vs['z']=0.0
	#图数据
	dg['Q'] = 100.0
	dg['precise'] = 1e-4
	dg['maxCount'] = 1000

#如果属性值是None,则给它设定默认值
def make_defalut_value(obj, property_name, property_value):
	if obj is None or property_name not in obj.attributes() or property_value is None:
		return
	elif obj[property_name] is None:
		obj[property_name] = property_value

#遍历图中的所有分支和节点,如果它的属性值为None,则给默认值
def default_graph_property(dg):
	for e in dg.es:
		make_defalut_value(e, 'id', 0)
		make_defalut_value(e, 'a0', 0.0)
		make_defalut_value(e, 'a1', 0.0)
		make_defalut_value(e, 'a2', 0.0)
		make_defalut_value(e, 'r', 0.0)
		make_defalut_value(e, 'q', 0.0)
		make_defalut_value(e, 'fq', 0.0)
		make_defalut_value(e, 'adjust_r', 0.0)
		make_defalut_value(e, 'adjust_h', 0.0)
		make_defalut_value(e, 'density', 1.2)
	for u in dg.vs:
		make_defalut_value(u, 'id', 0)
		make_defalut_value(u, 'p', 0.0)
		make_defalut_value(u, 'x', 0.0)
		make_defalut_value(u, 'y', 0.0)
		make_defalut_value(u, 'z', 0.0)
	make_defalut_value(dg, 'Q', 100.0)
	make_defalut_value(dg, 'precise', 1e-4)
	make_defalut_value(dg, 'maxCount', 1000)

#构建通风网络
def build_network(graph_datas, dg):
	if 'edges' not in graph_datas:
		return False
	elif len(graph_datas['edges']) == 0:
		return False

	#从词典中提取分支数据
	edges = graph_datas['edges']
	#构建有向图并返回节点编号、分支编号与igraph内部编号的映射关系
	nodes_map, edges_map = build_graph(edges, dg)
	init_graph_property(dg)
	set_graph_ids(dg, nodes_map, edges_map)
	for data in edges:
		i = edges_map[data['id']] 
		dg.es[i]['r'] = data['r']  
	if 'fans' in graph_datas:
		fans = graph_datas['fans']
		for data in fans:
			i = edges_map[data['eID']] 
			dg.es[i]['a0'] = data['a0']
			dg.es[i]['a1'] = data['a1']
			dg.es[i]['a2'] = data['a2']
	if 'qFixs' in graph_datas:
		qFixs = graph_datas['qFixs']
		for data in qFixs:
			i = edges_map[data['eID']]  
			dg.es[i]['fq'] = data['fq']
	if 'gates' in graph_datas:
		gates = graph_datas['gates']
		for data in gates:
			i = edges_map[data['eID']]  #igraph分支的内部编号
			dg.es[i]['adjust_r'] = dg.es[i]['adjust_r'] + data['r']

	#设置调节参数
	if 'Q' in graph_datas:
		dg['Q'] = graph_datas['Q']
	if 'precise' in graph_datas:
		dg['precise'] = graph_datas['precise']
	if 'maxCount' in graph_datas:
		dg['maxCount'] = graph_datas['maxCount']
	return True

#独立回路
class IndependentCycle:
	def __init__(self, dg, baseEdge, path):
		self.dg = dg
		self.baseEdge = baseEdge
		self.path = path[:]
		# print '基准分支:e%d, 路径:%s' % (self.baseEdge, str(self.path))
		self.coef = []
		#计算方向系数
		self.__initDirection()
		# print '方向系数:,self.coef
		# 判断回路是否可以参与迭代
		self.bCanDoIterate = self.__canDoIterate()
	def getBaseEdge(self):
		return self.baseEdge		
	def getCycleCoeff(self, i):
		if i < 0:
			return 0
		elif i == self.baseEdge:
			return 1
		elif i not in self.path:
			return 0
		else:
			return self.coef[self.path.index(i)]
	def iterate(self):
		dq, df = 0, 0
		if not self.bCanDoIterate:
			return False, dq, df
		else:
			# 计算回路风量修正量
			dq = self.__deltaQ()
			# 特殊处理风机分支
			# 保证风机分支的风量始终在抛物线的右侧(斜率小于0的一侧)
			self.__crackFan(dq)
			# 修正回路风量
			self.__increaseQ(dq)
			# 回路阻力代数和
			df = self.__f0() - self.__h0()
			return True, dq, df

	def __initDirection(self):
		if len(self.path) == 0:return
		u = self.dg.es[self.baseEdge].target
		d = 1
		for i in self.path:
			s, t = self.dg.es[i].tuple
			if d > 0:
				if s != u:
					d = -1*d
					u = s
				else:
					u = t
			else:
				if t != u:
					d = -1*d
					u = t
				else:
					u = s
			self.coef.append(d)
	def __canDoIterate(self):
		if self.__isFixQCycle() or self.__hasFixQ():
			return False
		elif self.__isAirCycle() and not self.__hasExtraF():
			return False
		return True
	def __isAirCycle(self):
		return is_zero_edge(self.dg.es[self.baseEdge])
	def __isFixQCycle(self):
		return is_fix_edge(self.dg.es[self.baseEdge])
	#检查回路中是否存在附加阻力(风机)
	def __hasExtraF(self):
		ret = False
		for i in self.path:
			#分支上有附加阻力(风机)
			if is_fan_edge(self.dg.es[i]):
				ret = True
				break
			else:
				pass
	def __hasFixQ(self):
		ret = False
		for i in self.path:
			if is_fix_edge(self.dg.es[i]):
				ret = True
				break
		return ret
	def __deltaQ(self):
		F0 = self.__f0()
		H0 = self.__h0()
		F1 = self.__f1()
		H1 = self.__h1()
		return -1.0*(F0-H0)/(F1-H1)
	def __increaseQ(self, dq):
		self.__increaseEdgeQ(self.baseEdge, dq)
		for i, c in zip(self.path, self.coef):
			self.__increaseEdgeQ(i, c*dq)
	def __increaseEdgeQ(self, i, dq):
		self.dg.es[i]['q'] = self.dg.es[i]['q'] + dq
	def __f0(self):
		return f0(self.dg.es[self.baseEdge]) + np.sum([f0(self.dg.es[i])*c for i,c in zip(self.path, self.coef)])
	def __f1(self):
		return f1(self.dg.es[self.baseEdge]) + np.sum([f1(self.dg.es[i])*abs(c) for i,c in zip(self.path, self.coef)])
	def __h0(self):
		return h0(self.dg.es[self.baseEdge]) + np.sum([h0(self.dg.es[i])*c for i,c in zip(self.path, self.coef)])
	def __h1(self):
		return h1(self.dg.es[self.baseEdge]) + np.sum([h1(self.dg.es[i])*c for i,c in zip(self.path, self.coef)])
	def __crackFan(self, dq):
		#如果基准分支上有风机,且斜率>0
		if h1(self.dg.es[self.baseEdge]) > 0:
			return 1000
		for i,c in zip(self.path, self.coef):
			if h1(self.dg.es[i]) > 0:
				dq = dq + c*1000
				break
		return dq
class VentNetwork:
	def __init__(self):
		self.dg = Graph(directed=True)
		self.sn = -1
		self.tn = -1
		self.airEdge = -1
	def graph(self):
		return self.dg
	def vSource(self):
		return self.sn
	def vTarget(self):
		return self.tn
	def vAir(self):
		return self.airEdge
	def addVirtualST(self):
		if self.sn > -1 or self.tn > -1:return
		#增加虚拟源点和汇点
		self.sn = add_virtual_source(self.dg)
		self.tn = add_virtual_target(self.dg)
		if self.sn < 0 or self.tn < 0:
			return
		else:
			default_graph_property(self.dg)
	def delVirtualST(self):
		if self.sn < 0 or self.tn < 0:return
		#删除虚拟源点和汇点以及虚拟分支
		self.dg.delete_vertices([self.sn, self.tn])
		self.sn, self.tn = -1, -1
	#增加虚拟的大气分支(虚拟的汇点->虚拟的源点)
	def addAirEdge(self):
		if self.sn < 0 or self.tn < 0 or self.airEdge >= 0:return
		#增加虚拟大气分支
		self.dg.add_edge(self.tn, self.sn)
		self.airEdge = self.dg.es.indices[-1]
		default_graph_property(self.dg)
	def delAirEdge(self):
		if self.airEdge < 0:return
		self.dg.delete_edges(self.airEdge)
		self.airEdge = -1
	def hPath(self, p):
		return np.sum([f0(e) for e in self.dg.es.select(p)])
	def filterVirutalEdges(self, p):
		return [e.index for e in self.dg.es.select(p) if not is_zero_edge(e)]
	def outArcFlow(self, u):
		return np.sum([dg.es[i]['q'] for i in self.dg.incident(u, mode=OUT)])
	def inArcFlow(self, u):
		return np.sum([dg.es[i]['q'] for i in self.dg.incident(u, mode=IN)])
	def countFixQ(self):
		return len([e.index for e in self.dg.es if is_fix_edge(e)])
	def fixQEdges(self):
		return [e.index for e in self.dg.es if is_fix_edge(e)]
	def fanEdges(self):
		return [e.index for e in self.dg.es if is_fan_edge(e)]
	def adjustNegativeEdge(self):
		ne = []
		for e in self.dg.es:
			if e['q'] < 0:
				e['q'] = -1.0*e['q']
				ne.append(e.index)
				self.dg.add_edge(e.target, e.source, **e.attributes())
		self.dg.delete_edges(ne)
def print_network(vnet):
	dg = vnet.graph()
	# print ('---------- igraph内部详细信息 ---------')
	# print (dg)
	print ('---------- 风量分配结果 ---------')
	for e in dg.es:
		print ('r(e%d)=%.3f\tq(e%d)=%.3f\th(e%d)=%.3f' % (e['id'],e['r'],e['id'],e['q'],e['id'],f0(e)))
def print_max_resistance_path(vnet, P):
	dg = vnet.graph()
	print ('P={%s}' % (','.join([str(dg.es[i]['id']) for i in P])))
def build_fixq_weight(vnet):
	#计算分支权重
	dg = vnet.graph()
	fixq_count = vnet.countFixQ()
	print ('固定风量个数:',fixq_count)
	if fixq_count == 0:
		# 人为固定第一条出边的风量为100
		i = dg.incident(vnet.vSource(), mode=OUT)[0]
		dg.es[i]['fq'] = 100
	#依次给图中的其他分支分配权重
	for e in dg.es:
		e['weight'] = e['fq'] if is_fix_edge(e) else 0.0
	if fixq_count == 0:
		# 恢复第一条出边的固定风量为0
		i = dg.incident(vnet.vSource(), mode=OUT)[0]
		dg.es[i]['fq'] = 0

def bound_max_flow(dg, s, t, Q, fixTotalQ=False):
	dg.add_vertex()
	s0 = dg.vs.indices[-1]
	dg.add_edge(s0, s)
	e0 = dg.es.indices[-1]
	dg.es[e0]['low'] = Q*1.0 if fixTotalQ else 0.0
	dg.es[e0]['high'] = Q*1.0
	# 添加一条t->s的分支,下界0,上界无穷大
	dg.add_edge(t, s0)
	ts = dg.es.indices[-1]
	dg.es[ts]['low'] = 0.0
	dg.es[ts]['high'] = DBL_MAX

	# 分支容量(默认无穷大)
	dg.es['capacity'] = DBL_MAX
	# 上界分支拆分后的分支映射记
	dg.es['lu'] = -1

	# 添加超级源汇
	dg.add_vertex()
	ss = dg.vs.indices[-1]
	dg.add_vertex()
	tt = dg.vs.indices[-1]
	for e in dg.es:
		if e['low'] > 0 and e['high'] >= e['low']:
			u, v = e.tuple
			dg.add_edge(ss, v)
			e1 = dg.es[dg.es.indices[-1]]
			dg.add_edge(u, tt)
			e2 = dg.es[dg.es.indices[-1]]
			e['capacity'] = e['high'] - e['low']
			e1['capacity'], e2['capacity'] = e['low'], e['low']
			e1['low'], e2['low'] = 0.0, 0.0
			e1['high'], e2['high'] = DBL_MAX, DBL_MAX
			e1['lu'], e2['lu'] = e.index, e.index
	flow = dg.maxflow(ss, tt, "capacity")
	max_flow = flow.value
	flow_map = flow.flow
	S = np.sum([e['low'] for e in dg.es])
	ret = abs(S - max_flow) < 1.0e-2
	if ret:
		for e in dg.es:
			e['flow'] = flow_map[e.index]
		edges = [e.index for e in dg.es if e['lu']>-1]
		aset = set()
		for i in edges:
			e = dg.es[dg.es[i]['lu']]
			if e.index not in aset:
				e['flow'] = e['low'] + flow_map[e.index]
				aset.add(e.index)
	del dg.es['capacity']
	del dg.es['lu']
	dg.delete_vertices([s0, ss, tt])
	return ret
def fixed_max_flow(dg, Q):
	sn = add_virtual_source(dg)
	tn = add_virtual_target(dg)
	if sn < 0 or tn < 0:
		return False
	else:
		for i in dg.incident(sn, mode=OUT):
			dg.es[i]['weight'] = 0.0
		for i in dg.incident(tn, mode=IN):
			dg.es[i]['weight'] = 0.0
			
		#增加3个属性数据
		dg.es['low'] = 0.1
		dg.es['high'] = DBL_MAX #表示无穷大
		dg.es['flow'] = 0.0
		for e in dg.es:
			if e['weight'] > 0:
				e['low'] = e['weight']
				e['high'] = e['weight']

		if bound_max_flow(dg, sn, tn, Q, False):
			for e in dg.es:
				e['weight'] = e['flow']
		#删除属性数据
		del dg.es['low']
		del dg.es['high']
		del dg.es['flow']
		dg.delete_vertices([sn, tn])
		return True
def ifq(vnet):
	dg = vnet.graph()
	# 增加权重属性数据
	dg.es['weight']=0.0
	# 构造分支权重
	build_fixq_weight(vnet)
	if not fixed_max_flow(dg, DBL_MAX):
		return False
	else:
		# 分配计算的风量
		for e in dg.es:
			e['q'] = e['weight']
	# 删除权重属性
	del dg.es['weight']
	return True


def build_tree_weight(vnet, speedUp):

	dg = vnet.graph()
	for e in dg.es:
		r, q = R(e), e['q'] 
		c = (1.0+r)*q if speedUp else r+1.0
		# 风机分支
		if is_fan_edge(e):
			c = c*LARGE_COEFF
		# 固定风量分支
		elif is_fix_edge(e):
			c = c*LARGE_COEFF*10
		# 虚拟大气分支
		elif e.index == vnet.vAir():
			c = c*LARGE_COEFF*100
		e['weight'] = c

#找最小生成树
def find_mst(vnet, speedUp):
	dg = vnet.graph()
	#增加权重属性数据
	dg.es['weight']=0.0
	#构造分支权重
	build_tree_weight(vnet, speedUp)
	#igraph的最小生成树算法需要传递一个数组,用来表示分支的权重
	weight = [e['weight'] for e in dg.es]
	tree = dg.spanning_tree(weights=weight, return_tree=False)
	#删除权重属性
	del dg.es['weight']
	#返回找到的树边
	return tree

#通过pred属性得到路径
def node_path_from_pred(pred, s, t):
	#记录路径(用节点表示)
	path = [t]
	u = t
	while pred[u] >= 0 and u != pred[u]:
		u = pred[u]
		path.append(u)

	if len(path) > 1:
		if path[-1] != s:
			path = []
		else:
			path.reverse()
	else:
		path = []
	return path

# 节点路径转换成分支路径
def node_path_to_edge_path(dg, node_path, directed=False):
	if len(node_path) < 2:
		return []

	# print node_path
	edge_path = []
	for u,v in zip(node_path[:-1], node_path[1:]):
		i = dg.get_eid(u, v, directed=directed, error=False)
		if i < 0:
			continue
		else:
			edge_path.append(i)
	return edge_path

# 深度优先搜索
def dfs_path(g, s, t):
	#igraph的python接口没有实现dfs,暂时用bfs替代
	ns, layer, pred = g.bfs(s, mode=OUT)
	# print ns, layer, pred
	# 返回节点路径
	return node_path_from_pred(pred, s, t)

#测试dfs
def test_dfs_path():
	dg = Graph(directed=True)
	dg.add_vertices(4)
	dg.add_edges([(0,1), (1,2), (1,3)])
	print (dfs_path(dg, 0, 3))
	print (dfs_path(dg, 0, 2))
	print (dfs_path(dg, 3, 0))
	print (dfs_path(dg, 2, 3))
	print ('-----------------------')
	print (node_path_to_edge_path(dg, dfs_path(dg, 0, 3)))
	print (node_path_to_edge_path(dg, dfs_path(dg, 0, 2)))
	print (node_path_to_edge_path(dg, dfs_path(dg, 3, 0)))
	print ('-----------------------')
	#转为无向图
	dg.to_undirected()
	print (dfs_path(dg, 2, 3))
	print (dfs_path(dg, 3, 2))

# test_dfs_path()

#找独立回路
def find_cycle(vnet, speedUp):
	# 查找最小生成树
	tree = find_mst(vnet, speedUp)
	if len(tree) == 0:
		return []

	dg = vnet.graph()
	g = dg.subgraph_edges(tree)
	# 查找所有的余支(通过集合的"差集"运算得到余支集合)
	edges_set = set([e.index for e in dg.es])  #所有分支集合
	tree_set = set(tree)  #树支集合
	left_tree_set = edges_set.difference(tree_set) #余支集合

	# 将树边转换成无向图
	g = dg.subgraph_edges(list(tree))
	g.to_undirected()
	# print g

	#独立回路数组
	cl = []

	# 对每个余支搜索回路
	for i in left_tree_set:
		# 无向图dfs搜索,v->u的路径(只有1条路径)
		u, v = dg.es[i].tuple
		node_path = dfs_path(g, v, u)
		# print v, '-->', u, ': ', node_path
		#节点路径转换为分支路径
		path = node_path_to_edge_path(dg, node_path, False)
		if len(path) == 0:
			continue
		else:
			# 构造独立回路对象(以余支i作为回路的基准分支)
			cycle = IndependentCycle(dg, i, path)
			# 添加回路到链表中
			cl.append(cycle)
	return cl

#判断数据的是否满足要求精度
def is_meet_error_precise(dvalues, precise):
	if len(dvalues) == 0:
		return True
	else:
		return np.max(np.abs(dvalues)) <= precise;
def iterate(vnet, count, speedUp):
	dg = vnet.graph()
	# 根据最小生成树查找独立回路
	cl = find_cycle(vnet, speedUp)
	if len(cl) == 0:
		return False
	else:
		# 迭代计算
		ret = False
		k = 0
		DQ, DF = [], []
		while not ret and k <= count:
			for cycle in cl:
				# 每个回路进行迭代
				each_ret, dq, df = cycle.iterate()
				# print '第%d次迭代: dq=%.3f, df=%.3f' % (k, dq, df)
				DQ.append(dq)
				DF.append(df)
			# 判断精度是否满足要求(风量精度和阻力精度)
			if is_meet_error_precise(DQ, dg['precise']) and is_meet_error_precise(DF, dg['precise']):
				ret = True
				break
			else:
				k = k+1
		# 回收内存
		del cl
		return ret


def vno(vnet):
	dg = vnet.graph()

	if not ifq(vnet):
		print ('初始化固定风量失败')
		return False
	else:
		# 添加虚拟大气分支
		vnet.addAirEdge()
		# 总的迭代次数
		totalCount = 0
		# 迭代结果
		ret = True
		while True:
			# 是否加速(如果20次计算后仍不收敛,开始加速)
			speedUp = (ret == False)
			# 迭代解算
			ret = iterate(vnet, 20, speedUp)
			# 总的迭代次数累加
			totalCount = totalCount + 20;

			if ret or totalCount > dg['maxCount']:
				break
		# 删除虚拟大气分支
		vnet.delAirEdge()
		# 返回迭代结果
		return ret

def build_pressure_weight(vnet):
	dg = vnet.graph()
	#计算分支权重
	# 以分支的阻力作为权重
	for e in dg.es:
		e['weight'] = f0(e)

def spfa(dg, s):
	# 最短路径搜索
	dists = dg.shortest_paths_dijkstra(s, weights='weight')
	if len(dists) == 0 or len(dists[0]) == 0:
		return

	dists = dists[0]
	# 遍历所有节点
	for v in dg.vs:
		if not np.isinf(dists[v.index]):
			v['dist'] = dists[v.index]

def back_spfa(dg, s):
	# 构造反向图(将原图分支反向)
	# print [(e.source, e.target, int(e['weight'])) for e in dg.es]
	edges = [(e.target, e.source) for e in dg.es]
	weight = [e['weight'] for e in dg.es]
	g = Graph(directed=True)
	g.add_vertices(len(dg.vs))
	g.add_edges(edges)
	g.es['weight'] = weight
	g.vs['dist'] = DBL_MAX
	# 执行spfa算法
	spfa(g, s)
	# 设置节点的dist属性
	dg.vs['dist'] = g.vs['dist'][:]
class QNode:
	def __init__(self, u, pred, g, h):
		self.u = u
		self.pred = pred
		self.g = g
		self.h = h
	def __lt__(self, other):
		f1 = self.g + self.h
		f2 = other.g + other.h
		# print abs(f1-f2), self.g, other.g, f1, f2
		if abs(f1-f2) < 1.0e-2:
			# print self.g, '<', other.g
			return self.g < other.g
		else:
			# print f1, '<', f2
			return f1 < f2
def a_star(dg, k, s, t):
	if s == t:
		return False

	pq = PriorityQueue()
	cnt = 0
	dg.vs[s]['pred'] = -1
	node = QNode(s, -1, 0, dg.vs[s]['dist'])
	pq.put(node)
	while not pq.empty():
		node = pq.queue[0]
		u = node.u
		dg.vs[u]['pred'] = node.pred
		# print 'pop: u=%d f=%.3f g=%.3f  h=%.3f' % (node.u, node.g+node.h, node.g, node.h)
		pq.get() # 类似pq.pop()
		if u == t:
			cnt = cnt + 1
		if cnt == k:
			break
		for i in dg.incident(u, mode=OUT):
			e = dg.es[i]
			v = e.target
			dg.vs[v]['pred'] = u
			child_node = QNode(v, u, node.g+e['weight'], dg.vs[v]['dist'])
			# print '\tpush: v=%d f=%.3f g=%.3f h=%.3f' % (child_node.u, child_node.g+child_node.h, child_node.g, child_node.h)
			pq.put(child_node)
	return cnt == k

# 权重逆转(取负值 或 用一个较大的数减去权重值)
def reverse_weight(dg):
	max_weight = 0.0
	for e in dg.es:
		e['weight'] = max_weight - e['weight']

# k最大阻力路线搜索
def mrp_k(vnet, k, s=-1, t=-1):
	dg = vnet.graph()
	if s < 0:
		s = vnet.vSource()
	if t < 0:
		t = vnet.vTarget()
	if k <= 0:
		k = 1
	dg.vs['dist'] = DBL_MAX
	dg.vs['pred'] = -1
	dg.es['weight'] = 1.0
	
	build_pressure_weight(vnet)
	reverse_weight(dg)
	back_spfa(dg, t)
	k_shortest_path = []
	if a_star(dg, k, s, t):
		k_shortest_path = node_path_from_pred(dg.vs['pred'], s, t)
	k_shortest_path = node_path_to_edge_path(dg, k_shortest_path, True)
	k_shortest_path = vnet.filterVirutalEdges(k_shortest_path)
	
	del dg.es['weight']
	del dg.vs['dist']
	del dg.vs['pred']
	return k_shortest_path

def mrp(vnet, s=-1, t=-1):
	return mrp_k(vnet, 1, s, t)

def standardize_dot_file_name(dot_file):
	path = os.path.splitext(dot_file)
	fname, ext = path[0], path[1][1:]
	if ext != 'dot':
		dot_file = '%s.dot' % (fname)
	# 合成png文件路径
	png_file = '%s.png' % (fname)
	# print dot_file, png_file
	return dot_file, png_file

# 将通风网络写入到dot文件中
# def write_vnet_network_to_dotfile(vnet, dot_file):
# 	# 有向图(流体网络)
# 	dg = vnet.graph()
#
# 	g=pgv.AGraph(directed=True,strict=True)
# 	g.graph_attr['rankdir']='BT'
# 	g.graph_attr['fontname']="SimSun"
# 	g.node_attr['fontname']="SimSun"
# 	g.edge_attr['fontname']="SimSun"
#
# 	for e in dg.es:
# 		if is_zero_edge(e):continue
#
# 		u = 'v%d' % (dg.vs[e.source]['id'])
# 		v = 'v%d' % (dg.vs[e.target]['id'])
# 		# 分支的属性
# 		edge_attr = {}
# 		# 分支编号
# 		edge_attr['label'] = 'e%d' % (e['id'])
# 		# 风阻R
# 		edge_attr['label'] = '%s\\lR=%.2f' % (edge_attr['label'], e['r'])
# 		# 风量Q
# 		edge_attr['label'] = '%s\\lQ=%.2f' % (edge_attr['label'], e['q'])
# 		# 阻力H
# 		edge_attr['label'] = '%s\\lH=%.2f' % (edge_attr['label'], f0(e))
#
#
# 		edge_attr['fontsize'] = '11'
#
# 		if is_fix_edge(e):
# 			edge_attr['color'] ="green"
# 			edge_attr['penwidth'] = '3'
# 		# 风机分支: 蓝色,粗线
# 		elif is_fan_edge(e):
# 			edge_attr['color'] ="blue"
# 			edge_attr['penwidth'] = '3'
#
# 		# style =\"dashed\", penwidth=5"
# 		g.add_edge(u, v, **edge_attr)
#
# 	# print g.string()
# 	# 写入dot文件
# 	g.write(dot_file)

# def write_path_to_dotfile(vnet, dot_file, P):
# 	# 有向图(流体网络)
# 	dg = vnet.graph()
# 	# 利用pygraphviz创建有向图
# 	g=pgv.AGraph(dot_file)
#
# 	f1 = lambda i:dg.vs[dg.es[i].source]['id']
# 	f2 = lambda i:dg.vs[dg.es[i].target]['id']
# 	path_edges = [('v%d' % f1(i), 'v%d' % f2(i)) for i in P]
# 	# print path_edges
# 	for u, v in path_edges:
# 		if g.has_edge(u, v):
# 			edge = g.get_edge(u, v)
# 			# print edge
# 			# 最大阻力路线分支: 虚线加粗
# 			edge.attr['style'] = 'dashed'
# 			edge.attr['penwidth'] = '3'
#
# 	# for edge in g.edges():
# 	# 	print edge.attr
# 	# 写入dot文件
# 	g.write(dot_file)

# 利用pygraphviz解析并绘制dot文件
# def draw_dot_file(dot_file, png_file):
# 	g=pgv.AGraph(dot_file)
# 	# 使用dot.exe进行布局
# 	g.layout('dot') # layout with dot
# 	# 绘制有向图
# 	g.draw(png_file) # write to file
# 	# g.draw('file.ps',prog='circo') # use circo to position,write PS file

# 查找多个回风井(汇点)的公共分支
def apm_common_edges(vnet):
	dg = vnet.graph()
	#查找所有出度等于0的节点
	nodes = dg.vs.select(_outdegree=0)
	if len(nodes) == 0:
		return []
	elif len(nodes) == 1 and nodes[0] == vnet.vTarget():
		nodes = [dg.es[i].source for i in dg.incident(nodes[0], mode=IN)]
	if len(nodes) < 2:return []

	arc_set = set()
	for s in nodes:
		ns, layer, pred = g.bfs(s, mode=IN)
		for u in ns:
			if pred[u] < 0:continue
			i = dg.get_eid(u, pred[v], directed=True, error=False)
			if i < 0:continue
			if i not in arc_set:
				arc_set.add(i)
			else:
				common_edges.append(i)
	return common_edges


def apm_mrp(vnet, fan, minDeltaH, maxDeltaH, n=1):
	if n<=0:n=1

	dg = vnet.graph()
	s, t = vnet.vSource(), dg.es[fan].source
	if t < 0:return []

	# 搜索最大阻力路线
	maxP = mrp(vnet, s, t)
	if len(maxP) == 0:return []

	maxH = vnet.hPath(maxP)

	more_maxP = []
	k = 1
	while len(more_maxP) < n:
		P = mrp_k(vnet, k, s, t)
		if len(P) == 0:
			break
		else:
			k = k+1
			H = vnet.hPath(P)
			deltaH = abs(maxH - H)
			if deltaH > minDeltaH and deltaH < maxDeltaH:
				more_maxP.append(P)
	return more_maxP

# def write_edge_path_pairs_to_dotfile(edge_path_pairs, dot_file):
# 	g=pgv.AGraph('strict digraph {}')
# 	g.graph_attr['rankdir']='LR'
# 	g.graph_attr['ranksep']='3.5'
# 	g.edge_attr['fontsize']='11'
# 	g.node_attr['style']='filled'
# 	g.node_attr['color']="skyblue"
# 	for i, node in enumerate(edge_path_pairs):
# 		u, v = 'e%d' % node[0], 'P%d' % node[1]
#
# 		# 分支的属性
# 		edge_attr = {}
# 		# 分支标签
# 		edge_attr['label'] = 'w%d=%.2f' % (i, node[2])
#
# 		# style =\"dashed\", penwidth=5"
# 		g.add_edge(u, v, **edge_attr)
#
# 	# print g.string()
# 	# 写入dot文件
# 	g.write(dot_file)

# 将通风网络写入到dot文件中
# def write_bipartite_graph_to_dotfile(dg, dot_file):
# 	g=pgv.AGraph('graph {}')
# 	g.graph_attr['rankdir']='BT'
# 	g.graph_attr['ranksep']='3.5'
# 	g.graph_attr['nodesep']='1.0'
# 	g.node_attr['style']='filled'
# 	g.node_attr['color']='skyblue'
# 	g.edge_attr['penwidth']='0.5'
# 	g.edge_attr['fontsize']='11'
#
# 	n = len(dg.vs) / 2
# 	for i in range(n):
# 		x_node = 'X(e%d)' % (dg.vs[i]['edge'])
# 		y_node = 'Y(e%d)' % (dg.vs[i]['edge'])
# 		# 分支的属性
# 		edge_attr = {}
# 		edge_attr['style']='invis'
# 		g.add_edge(x_node, y_node, **edge_attr)
#
# 	# 增加graphviz分支
# 	for e in dg.es:
# 		u = 'X(e%d)' % (dg.vs[e.source % n]['edge'])
# 		v = 'Y(e%d)' % (dg.vs[e.target % n]['edge'])
#
# 		# 分支的属性
# 		edge_attr = {}
#
# 		g.add_edge(u, v, **edge_attr)
#
# 	g.write(dot_file)


# def write_min_vertex_cover_to_dotfile(dg, dot_file, min_vertex_cover):
# 	# 利用pygraphviz创建有向图
# 	g=pgv.AGraph(dot_file)
#
# 	n = len(dg.vs) / 2
# 	for i in min_vertex_cover:
# 		u = 'X(e%d)' % (dg.vs[i % n]['edge'])
# 		if i >= n:
# 			u = 'Y(e%d)' % (dg.vs[i % n]['edge'])
# 		# 红色高亮最小顶点覆盖节点
# 		if g.has_node(u):
# 			node = g.get_node(u)
# 			node.attr['style']='filled'
# 			node.attr['color']="red"
#
# 	# 写入dot文件
# 	g.write(dot_file)

# 生成分支与通路的节点对
def build_edge_path_pairs(vnet, maxH, more_maxP):
	dg = vnet.graph()
	# 构造"分支-路径"对
	# edge_path_affect_dict = {}
	edge_path_pairs = []
	for i,P in enumerate(more_maxP):
		H = vnet.hPath(P)
		for j in P:
			# 分支可调
			if dg.es[j]['adjustable']:
				# 构造"分支-分支"对
				edge_path_pairs.append([j, i, maxH-H])
	print ('二分图节点个数:',len(edge_path_pairs))
	# print edge_path_pairs
	# print edge_path_affect_dict
	return edge_path_pairs

# 2维数组转换成1维的
def two_dim_to_one_dim(d):
	if len(d) == 0:return []
	m,n=np.shape(d)
	if m*n == 0:return []
	return np.resize(d, m*n)

def search_mrp(vnet, fan):
	dg = vnet.graph()


	maxP = mrp(vnet, vnet.vSource(), vnet.graph().es[fan].source)
	maxH = vnet.hPath(maxP)


	more_maxP = apm_mrp(vnet, fan, 10.0, DBL_MAX, 100)
	

	unadjust_edge_set = set(apm_common_edges(vnet))

	unadjust_edge_set.update(maxP)
	unadjust_edge_set.update(two_dim_to_one_dim(apm_mrp(vnet, fan, 0, 10.0, 100)))
	print ('不可调分支:',list(unadjust_edge_set))

	dg.es['dh'] = 0.0
	for i,P in enumerate(more_maxP):
		H = vnet.hPath(P)
		for x,j in enumerate(P):
			if j not in unadjust_edge_set:
				dg.es[j]['dh'] = maxH-H

	dg.es[i]['adjustable'] = False
	edges = set()
	for P in more_maxP:
		edges.update(P)
	edges.difference_update(unadjust_edge_set)
	for i in edges:
		dg.es[i]['adjustable'] = True

	print (edges)
	dg.es['pos'] = -1
	for i, e in enumerate(edges):
		dg.es[e]['pos'] = i

	return maxH, more_maxP, edges

# def build_bipartite_graph(vnet, fan):
# 	dg = vnet.graph()
# 	maxH, more_maxP, bipartite_nodes = search_mrp(vnet, fan)
# 	edge_path_pairs = build_edge_path_pairs(vnet, maxH, more_maxP)
#
# 	write_edge_path_pairs_to_dotfile(edge_path_pairs, 'dddd.dot')
# 	draw_dot_file('dddd.dot', 'dddd.png')
#
# 	g = Graph(directed=True)
# 	n = len(bipartite_nodes)
# 	g.add_vertices(2*n)
# 	g.vs["type"] = [0]*n+[1]*n
# 	for i,e in enumerate(bipartite_nodes):
# 		g.vs[i]['edge'] = e
# 		g.vs[i+n]['edge'] = e
# 		g.vs[i]['weight'] = dg.es[e]
# 		g.vs[i+n]['weight'] = dg.es[e]
# 	# 增加边(同一条路径上的分支互相影响构成一条边)
# 	for i,P in enumerate(more_maxP):
# 		for j in P:
# 			for k in P:
# 				u = dg.es[j]['pos']
# 				v = dg.es[k]['pos']
# 				# pos属性小于0表示该分支是不可调分支
# 				if j == k or u < 0 or v < 0:continue
# 				# 同一条路径上的分支互相影响
# 				g.add_edge(u, v+n)
#
# 	print (g)
#
# 	write_bipartite_graph_to_dotfile(g, 'cccc.dot')
#
# 	draw_dot_file('cccc.dot', 'cccc.png')
#
#
# 	return g

def solve_bipartite_graph(dg):
	
	dg.es['capacity'] = DBL_MAX
	# 增加虚拟的源点sn和汇点tn
	ss = add_virtual_source(dg)
	tt = add_virtual_target(dg)
	# 新增的虚拟分支容量为1
	for i in dg.incident(ss, mode=OUT):
		dg.es[i]['capacity'] = 1
	for i in dg.incident(tt, mode=IN):
		dg.es[i]['capacity'] = 1

	# 求最大流
	flow = dg.maxflow(ss, tt, capacity="capacity")
	print ('节点个数(包括虚拟源汇):', len(dg.vs))
	print ('最大流:', flow.value)
	min_vertex_cover = set()
	for i in flow.cut:
		u, v = dg.es[i].tuple
		if u != ss and u != tt:
			min_vertex_cover.add(u)
		if v != ss and v != tt:
			min_vertex_cover.add(v)

	print ('最小顶点覆盖:', set([dg.vs[i]['edge'] for i in min_vertex_cover]))

	dg.delete_vertices([ss, tt])


	write_min_vertex_cover_to_dotfile(dg, 'cccc.dot', min_vertex_cover)
	draw_dot_file('cccc.dot', 'cccc.png')

def test_priority_queue():
	class Node:
		def __init__(self,a,b):
			self.a = a
			self.b = b
		def __lt__(self, other):
			return self.a < other.a
		def __str__(self):
			return 'a=%d b=%d' % (self.a, self.b)
	pq = PriorityQueue()
	pq.put(Node(-1,2))
	pq.put(Node(-2,2))
	pq.put(Node(-3,2))
	pq.put(Node(-4,2))

	print (pq.get(), pq.get())

# def test_pygraphviz():
# 	g=pgv.AGraph(directed=True,strict=True)
# 	g.add_edge(1,2)
# 	g.add_edge(1,3)
# 	g.add_edge(2,4)
# 	g.add_edge(2,5)
# 	g.add_edge(5,6)
# 	g.add_edge(5,7)
# 	g.add_edge(3,8)
# 	g.add_edge(3,9)
# 	g.add_edge(8,10)
# 	g.add_edge(8,11)
# 	g.graph_attr['epsilon']='0.001'
# 	g.write('fooOld.dot')
# 	g.layout('dot') # layout with dot
# 	g.draw('fooOld.png') # write to file

def test_bipartite_graph(vnet, fan):
	dg = vnet.graph()
	g = build_bipartite_graph(vnet, fan)
	solve_bipartite_graph(g)

# def test_apm(vnet, fan):
# 	#
# 	more_maxP = apm_mrp(vnet, fan, 10.0, DBL_MAX, 10)
#
# 	for k, P in enumerate(more_maxP):
# 		H = vnet.hPath(P)
# 		print ('基于通路法的第%d最大阻力路线总阻力:%.3f' % (k+1, H))
# 		# 打印第k最大阻力路线
# 		print_max_resistance_path(vnet, P)
# 		if len(P) == 0:continue
# 		dot_file, png_file = standardize_dot_file_name('apm%d' % (k+1))
#
# 		write_vnet_network_to_dotfile(vnet, dot_file)
#
# 		write_path_to_dotfile(vnet, dot_file, P)
#
# 		draw_dot_file(dot_file, png_file)


def build_graph_data1():
	graph_datas = {
  "edges": [
	  #巷道id，阻力系数，起始点id，终止点id
    {"id": 1, "r": 0.375, "s": 1, "t": 2},
    {"id": 2, "r": 1.50, "s": 2, "t": 3},
    {"id": 3, "r": 2.0, "s": 2, "t": 4},
    {"id": 4, "r": 4.6875, "s": 3, "t": 6},
    {"id": 5, "r": 12.5, "s": 6, "t": 5},
    {"id": 6, "r": 1.7361, "s": 4, "t": 5},
    {"id": 7, "r": 0.5, "s": 4, "t": 8},
    {"id": 8, "r": 0.5, "s": 6, "t": 10},
    {"id": 9, "r": 0.5, "s": 3, "t":9},
    {"id": 10, "r": 0.5, "s":5 , "t":7 },
    {"id": 11, "r": 0.5, "s":7 , "t":8 },
    {"id": 12, "r": 0.5, "s":7 , "t": 9},
    {"id": 13, "r": 0.5, "s": 9, "t":11 },
    {"id": 14, "r": 0.5, "s": 11, "t":12 },
    {"id": 15, "r": 0.5, "s":8 , "t":16 },
    {"id": 16, "r": 0.5, "s": 11, "t":14 },
    {"id": 17, "r": 0.5, "s": 13, "t":14 },
    {"id": 18, "r": 0.5, "s": 10, "t":13 },
    {"id": 19, "r": 0.5, "s":13 , "t":16 },
    {"id": 20, "r": 0.5, "s": 10, "t":15 },
    {"id": 21, "r": 0.5, "s": 15, "t":19 },
    {"id": 22, "r": 0.5, "s": 16, "t":19 },
    {"id": 23, "r": 0.5, "s":15 , "t":17 },
    {"id": 24, "r": 0.5, "s": 17, "t":18 },
    {"id": 25, "r": 0.5, "s": 18, "t":20 },
    {"id": 26, "r": 0.5, "s": 19, "t":20 },
    {"id": 27, "r": 0.5, "s":17 , "t":21 },
    {"id": 28, "r": 0.5, "s": 18, "t":23 },
    {"id": 29, "r": 0.5, "s": 20, "t":22 },
    {"id": 30, "r": 0.5, "s": 21, "t":22 },
    {"id": 31, "r": 0.5, "s": 21, "t":24 }, 
    {"id": 32, "r": 0.5, "s": 23, "t": 24},
    {"id": 33, "r": 0.5, "s": 22, "t":23 },
    {"id": 34, "r": 0.5, "s": 24, "t":25 },
  ],
  "fans": [
    {"a0": 1046.3, "a1": 5.0, "a2": -0.85, "eID": 34},
    {"a0": 1046.3, "a1": 5.0, "a2": -0.85, "eID": 14}
  ],
  "maxCount": 1000,
  "precise": 0.0001
}
	return graph_datas

#构造网络数据2
def build_graph_data2():
	graph_datas = {
		"edges": [
			{"id":0,"r":0.08,"s":0,"t":1},
			{"id":1,"r":0.14,"s":0,"t":4},
			{"id":2,"r":0.20,"s":1,"t":2},
			{"id":3,"r":0.65,"s":2,"t":3},
			{"id":4,"r":0.20,"s":4,"t":3},
			{"id":5,"r":1.02,"s":1,"t":5},
			{"id":6,"r":1.0,"s":2,"t":6},
			{"id":7,"r":1.0,"s":3,"t":8},
			{"id":8,"r":1.20,"s":4,"t":9},
			{"id":9,"r":0.30,"s":5,"t":6},
			{"id":10,"r":0.32,"s":6,"t":7},
			{"id":11,"r":0.33,"s":8,"t":7},
			{"id":12,"r":0.30,"s":8,"t":9},
			{"id":13,"r":0.80,"s":5,"t":10},
			{"id":14,"r":0.12,"s":7,"t":10},
			{"id":15,"r":0.34,"s":9,"t":10},
			{"id":16,"r":0.13,"s":10,"t":11}
		],
		"fans": [
			{"a0":12955.830,"a1":407.387750,"a2":-3.87750,"eID":16}
		],
		"gates": [

		],
		"qFixs": [
			{"eID":10,"fq":33},
			{"eID":4,"fq":24}
		]
	}
	return graph_datas

def test_max_flow():
	dg = Graph(directed=True)
	dg.add_vertices(8)
	dg.add_edges([(0,4), (0,5), (0,7), (1,5), (2,4), (2,6), (3,5)])
	dg.es['capacity'] = DBL_MAX
	# 增加虚拟的源点s和汇点t
	dg.add_vertices(2)
	dg.add_edges([(8,0), (8,1), (8,2), (8,3)])
	dg.add_edges([(4,9), (5,9), (6,9), (7,9)])
	dg.es[7:]['capacity'] = 1
	print (dg.es['capacity'])

	ss, tt = 8, 9
	flow = dg.maxflow(ss, tt, capacity="capacity")
	print ('最大流:', flow.value)
	print ('最小割:', [dg.es[i].tuple for i in flow.cut])

def test_vno():

	graph_datas = build_graph_data1()

	#构造通风网络,读取并设置相关数据
	vnet = VentNetwork()
	if not build_network(graph_datas, vnet.graph()):
		print ('构造通风网络失败!!!')
	else:
		# print vnet.graph()
		print ('构造通风网络成功!!!')

		# 添加虚拟源汇,将网络变成单一源汇通风网络
		vnet.addVirtualST();

		ret = vno(vnet)
		print_network(vnet)

		# test_apm(vnet, 16)

		# test_bipartite_graph(vnet, 16)

		vnet.delVirtualST();

def test_mrp(vnet):

	for k in range(1,5):

		P = mrp_k(vnet, k, -1, -1)

		H = vnet.hPath(P)
		print ('第%d最大阻力路线总阻力:%.3f' % (k, H))

		print_max_resistance_path(vnet, P)

		if len(P) == 0:continue

		# 标准化dot文件名称(test.dot, test.png)
		dot_file, png_file = standardize_dot_file_name('mrp%d' % k)
		# 将通风网络写入到dot文件
		write_vnet_network_to_dotfile(vnet, dot_file)

		write_path_to_dotfile(vnet, dot_file, P)
		# 绘制并保存png图片
		draw_dot_file(dot_file, png_file)

if __name__=="__main__":
	test_vno()
	test_max_flow()
