from django.urls import path

from mines import views

urlpatterns = [
    path('MinesList/', views.MinesList.as_view(), name='MinesList'),
    path('MinesDetail/<int:pk>/', views.MinesDetail.as_view(), name='MinesDetail'),
    path('ThreeDMineTunnel/', views.ThreeDMineTunnelData.as_view(), name='ThreeDMineTunnel'),
    path('Run-Ventilation-Simulation/',views.RunVentilationSimulation.as_view(), name='RunVentilationSimulation')
]
