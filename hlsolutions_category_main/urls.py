from django.urls import path
from .controllers.category_controller import category_controller
from .middlewares.async_error_middleware import async_error_middleware

urlpatterns = [
    path('', async_error_middleware(category_controller.category_list_controller)),
    path('<uuid:id_category>/', async_error_middleware(category_controller.category_by_id)),
]