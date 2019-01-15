#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
import xmind

x = xmind.load('/Users/xmly/Desktop/center.xmind')

def treePaths(root,path,list):
    if not root:
        return []
    path += str(root.getTitle())
    if not root.getSubTopics():
        list.append(path)
    for topic in root.getSubTopics() or []:
        treePaths(topic,path+'->',list)
def main():
    for sheet in x.getSheets():
        path = ''
        list = []
        rootTopic = sheet.getRootTopic()
        treePaths(rootTopic,path,list)
        for onePath in list:
             print [node for node in onePath.split('->')]
if __name__ == '__main__':
    main()
