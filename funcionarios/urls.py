from django.urls import path
from .views import FuncionarioList, FuncionarioUpdate, FuncionarioDelete, FuncionarioCreate


urlpatterns = [
    path('', FuncionarioList.as_view(), name='list_funcionarios'),
    path('novo/', FuncionarioCreate.as_view(), name='create_funcionario'),
    path('editar/<int:pk>/', FuncionarioUpdate.as_view(), name='update_funcionario'),
    path('deletar/<int:pk>/', FuncionarioDelete.as_view(), name='delete_funcionario'),
]
