from rest_framework.routers import SimpleRouter
from gestioninvestigacionapp import views

from django.conf import settings
from django.conf.urls.static import static

from django.urls import path,include, re_path
from knox import views as knox_views


router = SimpleRouter()
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='knox_login'),
    path('register/', views.RegisterAPI.as_view(), name='register'),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
    
]

router.register(r'actividad', views.ActividadViewSet, 'Actividad')
router.register(r'archivo', views.ArchivoViewSet, 'Archivo')
router.register(r'archivoactividades', views.ArchivoActividadesViewSet, 'ArchivoActividades')
router.register(r'archivopostulaciones', views.ArchivoPostulacionesViewSet, 'ArchivoPostulaciones')
router.register(r'componente', views.ComponenteViewSet, 'Componente')
router.register(r'convocatoria', views.ConvocatoriaViewSet, 'Convocatoria')
router.register(r'curso', views.CursoViewSet, 'Curso')
router.register(r'departamento', views.DepartamentoViewSet, 'Departamento')
router.register(r'desafio', views.DesafioViewSet, 'Desafio')
router.register(r'entregable', views.EntregableViewSet, 'Entregable')
router.register(r'evaluacion', views.EvaluacionViewSet, 'Evaluacion')
router.register(r'notificciones', views.NotificcionesViewSet, 'Notificciones')
router.register(r'plantesis', views.PlantesisViewSet, 'Plantesis')
router.register(r'postulante', views.PostulanteViewSet, 'Postulante')
router.register(r'presupuesto', views.PresupuestoViewSet, 'Presupuesto')
router.register(r'reporte', views.ReporteViewSet, 'Reporte')
router.register(r'retroalimentacion', views.RetroalimentacionViewSet, 'Retroalimentacion')
router.register(r'retroalimentacionacttecnica', views.RetroalimentacionacttecnicaViewSet, 'Retroalimentacionacttecnica')
router.register(r'rubrica', views.RubricaViewSet, 'Rubrica')
router.register(r'user', views.UserViewSet, 'User')
router.register(r'actividadcronograma', views.ActividadcronogramaViewSet, 'Actividadcronograma')
router.register(r'actividadtecnica', views.ActividadtecnicaViewSet, 'Actividadtecnica')
router.register(r'postulacionpropuesta', views.PostulacionPropuestaViewSet, 'PostulacionPropuesta')
router.register(r'usercurso', views.UserCursoViewSet, 'UserCurso')
router.register(r'usuariodesafio', views.UsuarioDesafioViewSet, 'UsuarioDesafio')
router.register(r'estado', views.EstadoViewSet, 'Estado')
router.register(r'ubigeoDepartamento', views.ubigeoDepartamentoViewSet, 'dep')
router.register(r'ubigeoProvincia', views.ubigeoProvinciaViewSet, 'prov')
router.register(r'ubigeoDistrito', views.ubigeoDistritoViewSet, 'dist')

urlpatterns = urlpatterns +  router.urls
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

