from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..services.category_service import category_service
from ..errors.custom_exceptions import ServerError
import json

class CategoryController:
    """
    Controller class for managing categories.
    """

    @csrf_exempt
    def category_list_controller(self, request):
        """
        Controller method for retrieving all categories or creating a new category.

        Args:
            request: The HTTP request object.

        Returns:
            JsonResponse: The JSON response containing the list of categories or success message.

        Raises:
            ServerError: If there is an error while retrieving or creating the category.
        """
        if request.method == 'GET':
            try:
                result = category_service.get_all()
                return JsonResponse(result, safe=False, status=200)
            except ServerError as e:
                return JsonResponse({'error': str(e)}, status=e.code)
            
        elif request.method == 'POST':
            try:
                data = json.loads(request.body)
                result = category_service.create_category(data['name'])
                return JsonResponse({'message': 'Category created.'}, status=201)
            except ServerError as e:
                return JsonResponse({'error': str(e)}, status=e.code)

    @csrf_exempt
    def category_by_id(self, request, id_category):
        """
        Controller method for retrieving, updating, or deleting a category by its ID.

        Args:
            request: The HTTP request object.
            id_category: The ID of the category.

        Returns:
            JsonResponse: The JSON response containing the category details or success message.

        Raises:
            ServerError: If there is an error while retrieving, updating, or deleting the category.
        """
        if request.method == 'GET':
            try:
                result = category_service.get_by_id(id_category)
                return JsonResponse(result, safe=False, status=200)
            except ServerError as e:
                return JsonResponse({'error': str(e)}, status=e.code)
            
        elif request.method == 'PUT':
            try:
                data = json.loads(request.body)
                result = category_service.update_category(id_category, data['name'])
                return JsonResponse({'message': 'Category updated.'}, status=201)
            except ServerError as e:
                return JsonResponse({'error': str(e)}, status=e.code)

        elif request.method == 'DELETE':
            try:
                result = category_service.delete_category(id_category)
                return JsonResponse({}, status=204)
            except ServerError as e:
                return JsonResponse({'error': str(e)}, status=e.code)

category_controller = CategoryController()