# -*- coding: GB18030 -*-
from xml.etree.ElementTree import ElementTree,Element
import os,string
def read_xml(in_path):
  '''��ȡ������xml�ļ�
    in_path: xml·��
    return: ElementTree'''
  tree = ElementTree()
  tree.parse(in_path)
  return tree

def write_xml(tree, out_path):
  '''��xml�ļ�д��
    tree: xml��
    out_path: д��·��'''
  tree.write(out_path, encoding="utf-8",xml_declaration=True)

def if_match(node, kv_map):
  '''�ж�ĳ���ڵ��Ƿ�������д����������
    node: �ڵ�
    kv_map: ���Լ�����ֵ��ɵ�map'''
  for key in kv_map:
    if node.get(key) != kv_map.get(key):
      return False
  return True

#---------------search -----
def find_nodes(tree, path):
  '''����ĳ��·��ƥ������нڵ�
    tree: xml��
    path: �ڵ�·��'''
  return tree.findall(path)

def get_node_by_keyvalue(nodelist, kv_map):
  '''�������Լ�����ֵ��λ���ϵĽڵ㣬���ؽڵ�
    nodelist: �ڵ��б�
    kv_map: ƥ�����Լ�����ֵmap'''
  result_nodes = []
  for node in nodelist:
    if if_match(node, kv_map):
      result_nodes.append(node)
  return result_nodes

#---------------change -----
def change_node_properties(nodelist, kv_map, is_delete=False):
  '''�޸�/���� /ɾ�� �ڵ�����Լ�����ֵ
    nodelist: �ڵ��б�
    kv_map:���Լ�����ֵmap'''
  for node in nodelist:
    for key in kv_map:
      if is_delete:
        if key in node.attrib:
          del node.attrib[key]
      else:
        node.set(key, kv_map.get(key))

def change_node_text(nodelist, text, is_add=False, is_delete=False):
  '''�ı�/����/ɾ��һ���ڵ���ı�
    nodelist:�ڵ��б�
    text : ���º���ı�'''
  for node in nodelist:
    if is_add:
      node.text += text
    elif is_delete:
      node.text = ""
    else:
      node.text = text

def create_node(tag, property_map, content):
  '''����һ���ڵ�
    tag:�ڵ��ǩ
    property_map:���Լ�����ֵmap
    content: �ڵ�պϱ�ǩ����ı�����
    return �½ڵ�'''
  element = Element(tag, property_map)
  element.text = content
  return element

def add_child_node(nodelist, element):
  '''��һ���ڵ�����ӽڵ�
    nodelist: �ڵ��б�
    element: �ӽڵ�'''
  for node in nodelist:
    node.append(element)

def del_node_by_tagkeyvalue(nodelist, tag, kv_map):
  '''ͬ�����Լ�����ֵ��λһ���ڵ㣬��ɾ��֮
    nodelist: ���ڵ��б�
    tag:�ӽڵ��ǩ
    kv_map: ���Լ�����ֵ�б�'''
  for parent_node in nodelist:
    children = parent_node.getchildren()
    for child in children:
      if child.tag == tag and if_match(child, kv_map):
        parent_node.remove(child)

def change_Power_ChannelIndex_text(data,power,channelIndex):
    pararmlist = data.split(",")
    pararmlist[1] = "TransmitPower_1:" + str(power)
    pararmlist[2] = "ChannelIndex_1:" + str(channelIndex)
    data = ",".join(pararmlist)
    return data

def change_Modulation_DataEncode_ForwardReverse_text(data,ModulationType_text,DataEncodeType_text,ForwardReverseDataRate_text):
    #<Data>FreqSetting_1:0,TransmitPower_1:30,ChannelIndex_1:0,ModulationType_GB:3,DataEncodeType_GB:0,ForwardDataRate_GB:40,ReverseDataRate_GB:80</Data>
    pararmlist = data.split(",")
    pararmlist[1] = "TransmitPower_1:30" #���ʺ�Ƶ��ֵ�̶�
    pararmlist[2] = "ChannelIndex_1:10"
    pararmlist[3] = "ModulationType_GB:" + str(ModulationType_text)
    pararmlist[4] = "DataEncodeType_GB:" + str(DataEncodeType_text)
    pararmlist[5] = "ForwardDataRate_GB:" + str(ForwardReverseDataRate_text[0])
    pararmlist[6] = "ReverseDataRate_GB:" + str(ForwardReverseDataRate_text[1])
    data = ",".join(pararmlist)
    return data

def get_power_text(data):
    pararmlist = data.split(",")
    power = pararmlist[1].split(":")[1]
    return power



