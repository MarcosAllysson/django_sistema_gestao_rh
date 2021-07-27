from django.urls import path
from .views import FuncionarioList, FuncionarioUpdate


urlpatterns = [
    path('', FuncionarioList.as_view(), name='list_funcionarios'),
    path('editar/<int:pk>/', FuncionarioUpdate.as_view(), name='update_funcionarios'),
]
