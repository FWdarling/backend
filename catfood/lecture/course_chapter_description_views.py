from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from rest_framework.permissions import AllowAny

from .models import CourseChapterDescrption
from .serializers import CourseChapterDescrptionSerializer

from course.utils import is_student_within_course, is_teacher_teach_course

import json

from user.authentication import CatfoodAuthentication
from user.permissions import IsStudent, IsTeachingAssistant, IsTeacher, IsChargingTeacher


class ChapterDescriptionView(APIView):

    authentication_classes = [CatfoodAuthentication]
    permission_classes = [IsStudent |
                          IsTeachingAssistant | IsTeacher | IsChargingTeacher]

    def get(self, request, course_id, *args, **kwargs):
        user_character = request.user.character
        user_id = request.user.user_id
        # all within this class
        # TODO: change to match when comes to Python 3.10
        if user_character == 1:
            # charging teacher
            pass
        elif user_character == 2 or user_character == 3:
            # teacher or teaching assistant
            # check if this teacher teaches this course
            if not is_teacher_teach_course(user_id, course_id):
                return Response(dict({
                    "msg": "Forbidden. You are not within course."
                }), status=403)
        elif user_character == 4:
            # student
            # check if student is within this course
            if not is_student_within_course(user_id, course_id):
                return Response(dict({
                    "msg": "Forbidden. You are not within course."
                }), status=403)
        query_dict = request.query_params

        request_body = None
        request_has_body = False
        need_pagination = False
        pagination_page_size = -1
        pagination_page_num = -1

        request_body_unicode = request.body.decode('utf-8')
        if len(request_body_unicode) != 0:
            try:
                request_body = json.loads(request_body_unicode)
                request_has_body = True
            except json.decoder.JSONDecodeError:
                return Response(dict({
                    "msg": "Invalid JSON string provided."
                }), status=400)

        if request_has_body:
            # find out whether the user requested for pagination
            try:
                pagination_page_size = query_dict["itemCountOnOnePage"]
                pagination_page_num = query_dict["pageIndex"]
                need_pagination = True
            except KeyError:
                pass

        response = []
        all_courseChapterDescrption = CourseChapterDescrption.objects.filter(course_id=course_id)\
            .order_by('course_chapter_description_id')

        if need_pagination:
            pagination_start = (pagination_page_num - 1) * pagination_page_size
            pagination_end = pagination_page_num * pagination_page_size
            selected_courseChapterDescrption = all_courseChapterDescrption[pagination_start:pagination_end]
        else:
            selected_courseChapterDescrption = all_courseChapterDescrption
        for item in selected_courseChapterDescrption:
            response.append(CourseChapterDescrptionSerializer(item).data)
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request, course_id, format=None):
        user_character = request.user.character
        user_id = request.user.user_id
        # all within this class
        # TODO: change to match when comes to Python 3.10
        if user_character == 1:
            # charging teacher
            pass
        elif user_character == 2 or user_character == 3:
            # teacher or teaching assistant
            # check if this teacher teaches this course
            if not is_teacher_teach_course(user_id, course_id):
                return Response(dict({
                    "msg": "Forbidden. You are not within course."
                }), status=403)
        elif user_character == 4:
            # student
            # reject
            return Response(dict({
                "msg": "Forbidden. You are not the teacher."
            }), status=403)
        request_body_unicode = request.body.decode('utf-8')
        request_body = json.loads(request_body_unicode)
        new_courseChapterDescrption = CourseChapterDescrption(
            course_id=course_id,
            course_chapter_id=request_body["courseChapterId"],
            course_chapter_title=request_body["courseChapterTitle"],
            course_chapter_mooc_link=request_body["courseChapterMoocLink"],
        )

        if CourseChapterDescrption.objects\
                .filter(course_id=new_courseChapterDescrption.course_id, course_chapter_id=new_courseChapterDescrption.course_chapter_id).exists():
            return Response(dict({
                "error": "Course chapter already existed, use another API if you want to modify it."
            }), status=400)
        else:
            new_courseChapterDescrption.save()

        return Response(CourseChapterDescrptionSerializer(new_courseChapterDescrption).data, status=status.HTTP_201_CREATED)


class ChapterDescriptionIdView(APIView):

    authentication_classes = [CatfoodAuthentication]
    permission_classes = [IsStudent |
                          IsTeachingAssistant | IsTeacher | IsChargingTeacher]

    def get(self, request, course_id, course_chapter_id, format=None):
        user_character = request.user.character
        user_id = request.user.user_id
        # all within this class
        # TODO: change to match when comes to Python 3.10
        if user_character == 1:
            # charging teacher
            pass
        elif user_character == 2 or user_character == 3:
            # teacher or teaching assistant
            # check if this teacher teaches this course
            if not is_teacher_teach_course(user_id, course_id):
                return Response(dict({
                    "msg": "Forbidden. You are not within course."
                }), status=403)
        elif user_character == 4:
            # student
            # check if student is within this course
            if not is_student_within_course(user_id, course_id):
                return Response(dict({
                    "msg": "Forbidden. You are not within course."
                }), status=403)
        try:
            selected_courseChapterDescrption = CourseChapterDescrption.objects.get(course_id=course_id, course_chapter_id=course_chapter_id)
        except CourseChapterDescrption.DoesNotExist:
            return Response(dict({
                "msg": "Requested chapter does not exist.",
                "courseId": course_id,
                "course_chapter_id": course_chapter_id
            }), status=status.HTTP_404_NOT_FOUND)
        return Response(CourseChapterDescrptionSerializer(selected_courseChapterDescrption).data, status=status.HTTP_200_OK)

    def put(self, request, course_id, course_chapter_id, format=None):
        user_character = request.user.character
        user_id = request.user.user_id
        # all within this class
        # TODO: change to match when comes to Python 3.10
        if user_character == 1:
            # charging teacher
            pass
        elif user_character == 2 or user_character == 3:
            # teacher or teaching assistant
            # check if this teacher teaches this course
            if not is_teacher_teach_course(user_id, course_id):
                return Response(dict({
                    "msg": "Forbidden. You are not within course."
                }), status=403)
        elif user_character == 4:
            # student
            # reject
            return Response(dict({
                "msg": "Forbidden. You are not the teacher."
            }), status=403)
        request_body = None
        request_has_body = False

        request_body_unicode = request.body.decode('utf-8')
        if len(request_body_unicode) != 0:
            try:
                request_body = json.loads(request_body_unicode)
                request_has_body = True
            except json.decoder.JSONDecodeError:
                return Response(dict({
                    "msg": "Invalid JSON string provided."
                }), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(dict({
                "msg": "Expect a JSON, but got empty contents instead."
            }), status=status.HTTP_400_BAD_REQUEST)
        try:
            query_courseChapterDescrption = CourseChapterDescrption.objects.get(course_id=course_id, course_chapter_id=course_chapter_id)
            query_courseChapterDescrption.course_chapter_title = request_body["courseChapterTitle"]
            query_courseChapterDescrption.course_chapter_mooc_link = request_body["courseChapterMoocLink"]
            query_courseChapterDescrption.save()
        except CourseChapterDescrption.DoesNotExist:
            return Response(dict({
                "msg": "Requested course chapter does not exist.",
                "courseId": course_id,
                "announcement_id": id
            }), status=status.HTTP_404_NOT_FOUND)

        return Response(CourseChapterDescrptionSerializer(query_courseChapterDescrption).data, status=status.HTTP_200_OK)

    def delete(self, request, course_id, course_chapter_id, format=None):
        user_character = request.user.character
        user_id = request.user.user_id
        # all within this class
        # TODO: change to match when comes to Python 3.10
        if user_character == 1:
            # charging teacher
            pass
        elif user_character == 2 or user_character == 3:
            # teacher or teaching assistant
            # check if this teacher teaches this course
            if not is_teacher_teach_course(user_id, course_id):
                return Response(dict({
                    "msg": "Forbidden. You are not within course."
                }), status=403)
        elif user_character == 4:
            # student
            # reject
            return Response(dict({
                "msg": "Forbidden. You are not the teacher."
            }), status=403)
        try:
            courseChapterDescrption_to_delete = CourseChapterDescrption.objects.get(course_id=course_id, course_chapter_id=course_chapter_id)
            courseChapterDescrption_to_delete.delete()
        except CourseChapterDescrption.DoesNotExist:
            return Response(dict({
                "msg": "Requested announcement does not exist.",
                "courseId": course_id,
                "announcement_id": id
            }), status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
