from bdb import set_trace
from gc import get_objects
from django.shortcuts import render
from main.models import Operational, User
from main.serializers import (
    LoginSerializer,
    OperationalSerializer,
    UserSerializer,
)
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login as django_login, logout as django_logout
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework import mixins, generics
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser
from django.http import HttpResponse
from rest_framework import generics
from wsgiref.util import FileWrapper


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        django_login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=200)


class LogoutView(APIView):
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        django_logout(request)
        return Response({"Message": "successfully logout"}, status=204)


class OperationalRegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            u = User.objects.all().last()
            id = u.id
            obj = User.objects.get(pk=id)
            obj.is_operational = True
            obj.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


# from rest_framework_simplejwt.tokens import RefreshToken
# from .utils import Util
# from django.contrib.sites.shortcuts import get_current_site
# from django.urls import reverse


class ClientRegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            u = User.objects.all().last()
            id = u.id
            obj = User.objects.get(pk=id)
            obj.is_client = True
            obj.save()
            # profile = Profile.objects.create(
            #     user=User.objects.last(),

            # user = User.objects.get(email=request.data['email'])
            # token = RefreshToken.for_user(user).access_token
            # current_site = get_current_site(request).domain
            # relativeLink = reverse('email-verify')
            # absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
            # email_body = 'Hi '+user.username + \
            #     ' Use the link below to verify your email \n' + absurl
            # data = {'email_body': email_body, 'to_email': user.email,
            #         'email_subject': 'Verify your email'}

            # Util.send_email(data)
            # return Response(user_data, status=status.HTTP_201_CREATED)
            #     phone_number=request.data["phone_number"],
            #     email=request.data["email"],

            # )
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

# class VerifyEmail(generics.GenericAPIView):
#     def get(self):
#         pass


class UploadFile(APIView):
    # permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        import ipdb;set_trace()
        a = request.data["user"]
        if User.objects.get(id=a).is_operational is True:
            file_serializer = OperationalSerializer(data=request.data)
            if file_serializer.is_valid():
                file_serializer.save()
                return Response(file_serializer.data, status=201)
            else:
                return Response(file_serializer.errors, status=400)
        else:
            return Response({"message": "please provide operational user"})


class DownloadView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, format=None):
        # import ipdb; ipdb.set_trace()
        queryset = Operational.objects.get(pk=pk)
        file_handle = queryset.file.path
        document = open(file_handle, 'rb')
        response = HttpResponse(FileWrapper(document),
                                content_type='application/msword')
        response['Content-Disposition'] = 'attachment; filename="%s"' % queryset.file.name
        return response


class UserListView(generics.GenericAPIView, mixins.ListModelMixin, mixins.DestroyModelMixin):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):

        params = request.query_params
        print(params)
        if not "pk" in kwargs:
            return self.list(request)
        post = get_object_or_404(User, pk=kwargs["pk"])
        return Response(UserSerializer(post).data, status=200)

    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            post = serializer.save()
            return Response(UserSerializer(post).data, status=201)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk=None):
        return self.destroy(request, pk)


class OperationalListView(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = OperationalSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Operational.objects.all()

    def get(self, request, *args, **kwargs):
        if request.user.is_client is True:
            params = request.query_params
            print(params)
            if not "pk" in kwargs:
                return self.list(request)
            post = get_object_or_404(Operational, pk=kwargs["pk"])
            return Response(OperationalSerializer(post).data, status=200)
        else:
            return Response({"message": "only client user allow"})

    def post(self, request):
        data = request.data
        serializer = OperationalSerializer(data=data)
        if serializer.is_valid():
            post = serializer.save()
            return Response(OperationalSerializer(post).data, status=201)
        return Response(serializer.errors, status=400)
