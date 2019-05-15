from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .serializers import MovieSerializer, CommentSerializer, GenreSerializer
from .serializers import ActorSerializer, StaffSerializer, DirectorSerializer
from movies.models import Movie, Comment, Genre
from people.models import Actor, Director, Staff
from accounts.models import Temperature, GenrePreference


@api_view(['GET'])
def movie_list(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    serializer = MovieSerializer(movie, many=False)
    return Response(serializer.data)


# TODO 포스트 쪽에 평점 연결.
@api_view(['GET', 'POST'])
def comment_list(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == 'POST':
        if request.user.is_authenticated:
            print(request.user.id)
            request.data.update(user=request.user.id)
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()  # 평점이 등록되는 순간
                # 기존 해당 장르선호도 존재하는지 확인.(복수개의 장르가 존재 가능)
                genres = movie.genre.all()
                for genre in genres:
                    try:
                        gp = GenrePreference.objects.get(Q(user_id=request.user.id) & Q(genre_id=genre.id))
                    except:
                        # 없다면 장르선호도 생성
                        gp = GenrePreference.objects.create(user_id=request.user.id, genre=genre)
                    # 평점에 따라 스코어 부여
                    user_score = int(request.data.get('score'))
                    if user_score < 5:
                        gp.score -= user_score
                    else:
                        gp.score += user_score
                    gp.save()
                return Response(serializer.data)
        else:
            return Response({'message': '인증되지 않은 사용자입니다.'})
    else:
        comments = movie.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


@api_view(['GET', 'DELETE', 'PUT'])
def comment_detail(request, movie_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == 'GET':
        serializer = CommentSerializer(comment, many=False)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        comment.delete()
        return Response({'message': '해당 평점이 삭제되었습니다.'})
    elif request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    return Response({'message': '유효한 방법을 통해 요청하세요.'})


@api_view(['GET'])
def genre_list(request):
    genres = Genre.objects.all()
    serializer = GenreSerializer(genres, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def genre_movies(request, genre_id):
    genre = get_object_or_404(Genre, pk=genre_id)
    movies = genre.movies.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def actors(request):
    actors = Actor.objects.all()
    serializer = ActorSerializer(actors, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def directors(request):
    directors = Director.objects.all()
    serializer = DirectorSerializer(directors, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def staff(request):
    staff = Staff.objects.all()
    serializer = StaffSerializer(staff, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def actor_detail(request, actor_id):
    actor = get_object_or_404(Actor, pk=actor_id)
    serializer = ActorSerializer(actor, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def director_detail(request, director_id):
    director = get_object_or_404(Director, pk=director_id)
    serializer = DirectorSerializer(director, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def staff_detail(request, staff_id):
    staff = get_object_or_404(Staff, pk=staff_id)
    serializer = StaffSerializer(staff, many=False)
    return Response(serializer.data)

