from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404


from .models import CustomUser, Question, Answer
from .serializers import UserRegistrationSerializer, UserLoginSerializer, \
                         QuestionSerializer, AnswerSerializer
# Create your views here.

class UserRegistrationAPIView(APIView):
    """
    Creates a new user.
    
    Parameters:
    - `username`: the username of the user
    - `first_name`: the first name of the user
    - `last_name`: the last name of the user
    - `email`: the email address of the user
    - `password`: the password of the user
    
    Returns:
    - `201 Created`: the user has been successfully created
    - `400 Bad Request`: if the request contains invalid data
    """

    def post(self, request, *args, **kwargs):
        try:
            serializer = UserRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                user_data = serializer.validated_data
                user=CustomUser(username=user_data['username'], first_name=user_data['first_name'], last_name=user_data['last_name'],email=user_data['email'])
                user.set_password(user_data['password'])
                user.save()
                return Response("User Registered Successfully", status.HTTP_201_CREATED)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status.HTTP_400_BAD_REQUEST)

class UserLoginAPIView(APIView):

    """
    Logs in a user.

    Parameters:
    - `username`: the username of the user
    - `password`: the password of the user

    Returns:
    - `202 Accepted`: the user has been successfully logged in
    - `401 Unauthorized`: if the username or password is incorrect
    - `400 Bad Request`: if the request contains invalid data
    """
    
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username=serializer.validated_data['username']
            password=serializer.validated_data['password']
            try:
                user=authenticate(request, username=username, password=password)
                if user:
                    return Response("User Logged in Successfully", status.HTTP_202_ACCEPTED)
                return Response("Invalid credentials", status.HTTP_401_UNAUTHORIZED)
            except Exception as e:
                return Response(str(e), status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

class UserLogoutAPIView(APIView):

    """
    Logs out a user.

    Parameters:
    - `username`: the username of the user
    - `password`: the password of the user

    Returns:
    - `202 Accepted`: the user has been successfully logged out
    - `401 Unauthorized`: if the username or password is incorrect
    - `400 Bad Request`: if the request contains invalid data
    """
    
    def post(self, request, *args, **kwargs):
        logout(request)
        return Response("User Logged out Successfully", status.HTTP_202_ACCEPTED)


class PostQuestionView(APIView):
    """
    Posts a question.

    Parameters:
    - `title`: the title of the question

    Returns:
    - `201 Created`: the question has been successfully posted
    - `400 Bad Request`: if the request contains invalid data
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            serializer = QuestionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

class ListQuestionsView(APIView):
    """
    Lists all questions.

    Returns:
    - `200 Ok`: a list of all questions
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        try:
            questions = Question.objects.all().order_by('-created_at')
            serializer = QuestionSerializer(questions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class PostAnswerView(APIView):
    """
    Allows authenticated users to post an answer to a specific question.

    Parameters:
    - `request`: the HTTP request object
    - `question_id`: the ID of the question to which the answer is being posted

    Returns:
    - `201 Created`: if the answer has been successfully posted
    - `400 Bad Request`: if the request data is invalid or an error occurs
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, question_id):
        try:
            question = get_object_or_404(Question, id=question_id)
            serializer = AnswerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user, question=question)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

class LikeAnswerView(APIView):
    """
    Allows authenticated users to like an answer to a specific question.

    Parameters:
    - `request`: the HTTP request object
    - `answer_id`: the ID of the answer to which the like is being posted

    Returns:
    - `201 Created`: if the like has been successfully posted
    - `400 Bad Request`: if the user has already liked the answer
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, answer_id):
        try:
            answer = get_object_or_404(Answer, id=answer_id)
            if request.user in answer.likes.all():
                return Response({"detail": "You already liked this answer."}, status=status.HTTP_400_BAD_REQUEST)
            answer.likes.add(request.user)
            return Response({"detail": "Answer liked."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)