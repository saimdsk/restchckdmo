from AG_SADCeFarms import settings
from database.models import TodoList
from .todo_serializers import TodoListSerializer, TodoListUpdateSerializer

from django.http import Http404, HttpResponse, JsonResponse
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.middleware.csrf import get_token
from django.db import IntegrityError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

#
import logging
import traceback
import sys
import json

import hashlib
from datetime import datetime

logger = logging.getLogger(__name__)


class GetTodoList(APIView):
    """
        Get TodoLists for the Todo List Manager
    """
    def get(self, request, todo_list_guid=None, program_type_guid=None, format=None):
        if todo_list_guid is not None:
            try:
                todolists = TodoList.objects.get(todo_list_guid=todo_list_guid)
                print 'TODO:',todolists
                serializer = TodoListSerializer(todolists)
            except TodoList.DoesNotExist:
                raise Http404
        else:
            todolists = TodoList.objects.all().order_by('todo_list_title')

            serializer = TodoListSerializer(todolists, many=True)
        return JsonResponse(serializer.data, safe=False) #Response(serializer.data)


class UpdateTodoList(APIView):
    """
        Update TodoList (add,update,delete) for the Todo List Managaer
    """

    def put(self, request, todo_list_guid=None):
        if todo_list_guid == None:
            error = "No Todo List ID provided"
            #logger.debug(authAdminErrors[error]['d_msg'])
            return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)
        print"TODOLIST PUT REQUEST:", request.data
        try:
            todolist_item = TodoList.objects.get(todo_list_guid=todo_list_guid)
            print(">> REQUEST DATA IN:", request.data)
            #if not isinstance(request.data['todo_list_json'], basestring):
            print '>>>>>', type(request.data['todo_list_json'])
            #request.data['todo_list_json'] = str(request.data['todo_list_json'])

            serializer = TodoListUpdateSerializer(todolist_item, data=request.data)
            print ">>> AFTER USER SERIALIZER"

            if serializer.is_valid():
                serializer.save()
                print ">>VALID SERIALIZER FOR TODOLIST", serializer.data
                return JsonResponse(serializer.data, safe=False)
            print ">> SERIALIZER MUST BE BAD", serializer.errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except TodoList.DoesNotExist:
            error = "Todo List Item Does Not Exist"
            #logger.debug(authAdminErrors[error]['d_msg'])
            return Response('{"error": "' + error + '"}', status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            print e
            #logger.debug(authAdminErrors[error]['d_msg'])
            return Response('{"error": "Not valid JSON"}', status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        print("USER POST REQUEST:", request.data)
        # Make sure title is not empty
        if 'todo_list_title' not in request.data:
            error = "Missing Todo List Title"
            return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)
        if request.data['todo_list_title'] == '':
            error = "Missing Todo List Title"
            return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # check to see if TodoList with that Title already exists
            try:
                todolistitem = TodoList.objects.get(todo_list_title=request.data['todo_list_title'])
                # If exception isn't thrown, that means todolist title already exists.  So error out.
                error = "ToDo List by the same title already exists"
                return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)
            except TodoList.DoesNotExist:
                # We are good to create a new todolist
                # Set status to created
                #if not isinstance(request.data['todo_list_json'], basestring):
                #    print '>>>>>', type(request.data['todo_list_json'])
                #    request.data['todo_list_json'] = json.dumps(request.data['todo_list_json'])
                serializer = TodoListUpdateSerializer(data=request.data)
                print "SERIALIZED TODOLIST:", serializer
                if serializer.is_valid():
                    serializer.save()
                    print ">>VALID SERIALIZER FOR TODOLIST", serializer.data
                    return JsonResponse(serializer.data, safe=False)
                else:
                    error = "err-a006"
                    return Response('{"error": "' + error + '"}', status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, todo_list_guid=None, format=None):
        print 'DELETE TODOLIST',todo_list_guid
        print todo_list_guid
        try:
            todolistitem = TodoList.objects.get(todo_list_guid=todo_list_guid)
            todolistitem.delete()
            return Response("success", status=status.HTTP_200_OK )
        except TodoList.DoesNotExist:
            error = "Todo List Item Does Not Exist"
            return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)