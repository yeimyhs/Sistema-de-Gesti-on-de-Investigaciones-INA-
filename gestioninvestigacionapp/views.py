from rest_framework.viewsets import ModelViewSet
from gestioninvestigacionapp.serializers import ActividadSerializer, ArchivoSerializer, ArchivoActividadesSerializer, ArchivoPostulacionesSerializer, ComponenteSerializer, ConvocatoriaSerializer, CursoSerializer, DepartamentoSerializer, DesafioSerializer, EntregableSerializer, EvaluacionSerializer, NotificcionesSerializer, PlantesisSerializer, PostulanteSerializer, PresupuestoSerializer, ReporteSerializer, RetroalimentacionSerializer, RetroalimentacionacttecnicaSerializer, RubricaSerializer, UserSerializer, ActividadcronogramaSerializer, ActividadtecnicaSerializer, PostulacionPropuestaSerializer, UserCursoSerializer, UsuarioDesafioSerializer
from gestioninvestigacionapp.serializers import *
from gestioninvestigacionapp.models import Actividad, Archivo, ArchivoActividades, ArchivoPostulaciones, Componente, Convocatoria, Curso, Departamento, Desafio, Entregable, Evaluacion, Notificciones, Plantesis, Postulante, Presupuesto, Reporte, Retroalimentacion, Retroalimentacionacttecnica, Rubrica, Actividadcronograma, Actividadtecnica, PostulacionPropuesta, UserCurso, UsuarioDesafio
from .models import CustomUser


from rest_framework import generics
from rest_framework.response import Response
from knox.models import AuthToken

from knox.views import LoginView as KnoxLoginView
from rest_framework import status
from django.contrib.auth import login
from rest_framework import status, permissions
from django.http import JsonResponse

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "user": serializer.data,
            
            "token": AuthToken.objects.create(user)[1]
        })
        
class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        # Inicializar el serializer con los datos enviados
        serializer = CustomAuthTokenSerializer(data=request.data)

        # Intentar validar el serializer
        if not serializer.is_valid():
            # Construir una respuesta de error uniforme en JSON
            errors = serializer.errors
            return JsonResponse(
                {
                    "success": False,
                    "error": {
                        "code": "invalid_data",
                        "message": "Se encontraron errores en los datos enviados.",
                        "details": errors,  # Esto incluye los errores del serializer
                    }
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Recuperar el usuario autenticado desde el serializer
        user = serializer.validated_data["user"]

        # Iniciar sesión
        login(request, user)

        # Obtener la respuesta estándar de Knox
        response = super(LoginView, self).post(request, format=None)
        expiry = response.data.get("expiry")
        # Serializar la información del usuario
        user_serializer = CustomUserSerializer(user)

        # Responder con un JSON que combine el token y la información del usuario
        return JsonResponse(
            {   
                "success": True,
                "expiry": expiry,
                "token": response.data["token"],
                "user": user_serializer.data,
            },
            status=status.HTTP_200_OK,
        )
        
class ActividadViewSet(ModelViewSet):
    queryset = Actividad.objects.order_by('pk')
    serializer_class = ActividadSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['idactividad', 'tipo', 'fechaentrega', 'fechacreacion', 'activo', 'estado', 'idproyecto', 'idproyecto__titulo']
    search_fields = ['titulo', 'descripcion', 'idproyecto__titulo']
    
class ArchivoViewSet(ModelViewSet):
    queryset = Archivo.objects.order_by('pk')
    serializer_class = ArchivoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['idarchivo', 'activo', 'fechacreacion', 'idconvocatoria', 'idconvocatoria__titulo', 'idproyecto', 'idproyecto__titulo']
    search_fields = ['nombre', 'ubicacion', 'idconvocatoria__titulo', 'idproyecto__titulo']
    
class ArchivoActividadesViewSet(ModelViewSet):
    queryset = ArchivoActividades.objects.order_by('pk')
    serializer_class = ArchivoActividadesSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['idarchivo', 'activo', 'fechacreacion', 'idactividad', 'idactividad__titulo']
    search_fields = ['nombre', 'ubicacion', 'idactividad__titulo']

class ArchivoPostulacionesViewSet(ModelViewSet):
    queryset = ArchivoPostulaciones.objects.order_by('pk')
    serializer_class = ArchivoPostulacionesSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['idarchivo', 'activo', 'fechacreacion', 'idconvocatoria', 'idproyecto', 'idproyecto__titulo']
    search_fields = ['nombre', 'ubicacion', 'idproyecto__titulo']

class ComponenteViewSet(ModelViewSet):
    queryset = Componente.objects.order_by('pk')
    serializer_class = ComponenteSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['idcomponente', 'numero', 'idproyecto', 'idproyecto__titulo']
    search_fields = ['idproyecto__titulo']

class ConvocatoriaViewSet(ModelViewSet):
    queryset = Convocatoria.objects.order_by('pk')
    serializer_class = ConvocatoriaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['idconvocatoria', 'activo', 'estado', 'fechacreacion', 'idactividad', 'idactividad__titulo']
    search_fields = ['titulo', 'descripcion', 'objetivogeneral', 'idactividad__titulo']

class CursoViewSet(ModelViewSet):
    queryset = Curso.objects.order_by('pk')
    serializer_class = CursoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['idcurso', 'anioacademico', 'semestre', 'activo', 'estado', 'iddepartamento', 'iddepartamento__nombre']
    search_fields = ['titulo', 'coordinador', 'iddepartamento__nombre']

class DepartamentoViewSet(ModelViewSet):
    queryset = Departamento.objects.order_by('pk')
    serializer_class = DepartamentoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['iddepartamento', 'estado', 'activo', 'fechacreacion']
    search_fields = ['nombre', 'lugar', 'email', 'director']


class DesafioViewSet(ModelViewSet):
    queryset = Desafio.objects.order_by('pk')
    serializer_class = DesafioSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['idproyecto', 'estado', 'activo', 'fechacreacion', 'idconvocatoria', 'idconvocatoria__titulo', 'idcurso', 'idcurso__titulo']
    search_fields = ['titulo', 'descripcion', 'idconvocatoria__titulo', 'idcurso__titulo']


class EntregableViewSet(ModelViewSet):
    queryset = Entregable.objects.order_by('pk')
    serializer_class = EntregableSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['idactividadtecnica', 'comentario', 'idactividadtecnica__titulo']
    search_fields = ['comentario', 'idactividadtecnica__titulo']

class EvaluacionViewSet(ModelViewSet):
    queryset = Evaluacion.objects.order_by('pk')
    serializer_class = EvaluacionSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['idevaluacion', 'idplanformacion', 'idplanformacion__titulo']
    search_fields = ['comentario', 'idplanformacion__titulo']

class NotificcionesViewSet(ModelViewSet):
    queryset = Notificciones.objects.order_by('pk')
    serializer_class = NotificcionesSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['idnotificacion', 'activo', 'fechacreacion', 'iduser']
    search_fields = ['titulo', 'descripcion']


class PlantesisViewSet(ModelViewSet):
    queryset = Plantesis.objects.order_by('pk')
    serializer_class = PlantesisSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['idplanformacion', 'idproyecto', 'idproyecto__titulo']
    search_fields = ['titulo', 'abstract', 'idproyecto__titulo']


class PostulanteViewSet(ModelViewSet):
    queryset = Postulante.objects.order_by('pk')
    serializer_class = PostulanteSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['iduser', 'activo', 'fechacreacion', 'idproyecto', 'idproyecto__titulo']
    search_fields = ['nombres', 'apellidos', 'email', 'institucion', 'idproyecto__titulo']


class PresupuestoViewSet(ModelViewSet):
    queryset = Presupuesto.objects.order_by('pk')
    serializer_class = PresupuestoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['idpresupuesto', 'idproyecto', 'idproyecto__titulo']
    search_fields = ['partida', 'idproyecto__titulo']


class ReporteViewSet(ModelViewSet):
    queryset = Reporte.objects.order_by('pk')
    serializer_class = ReporteSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    ilterset_fields = ['idreporte', 'idactividad', 'idactividad__titulo']
    search_fields = ['idactividad__titulo']


class RetroalimentacionViewSet(ModelViewSet):
    queryset = Retroalimentacion.objects.order_by('pk')
    serializer_class = RetroalimentacionSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['idretroalimentacion', 'idreporte', 'idreporte__idactividad__titulo']
    search_fields = ['comentario', 'idreporte__idactividad__titulo']


class RetroalimentacionacttecnicaViewSet(ModelViewSet):
    queryset = Retroalimentacionacttecnica.objects.order_by('pk')
    serializer_class = RetroalimentacionacttecnicaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['idactividadtecnica', 'fecha', 'comentario', 'idactividadtecnica__titulo']
    search_fields = ['comentario', 'idactividadtecnica__titulo']

class RubricaViewSet(ModelViewSet):
    queryset = Rubrica.objects.order_by('pk')
    serializer_class = RubricaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['idproyecto', 'idproyecto__nombre']
    search_fields = ['idproyecto__nombre']

class UserViewSet(ModelViewSet):
    queryset = CustomUser.objects.order_by('pk')
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = [
        'id', 'nombres', 'apellidos', 'telefono', 'activo', 
        'instituto', 'pais', 'ciudad', 'email', 'email_verified_at'
    ]
    
    search_fields = [
        'nombres', 'apellidos', 'telefono', 
        'instituto', 'pais', 'ciudad', 'email'
    ]
class ActividadcronogramaViewSet(ModelViewSet):
    queryset = Actividadcronograma.objects.order_by('pk')
    serializer_class = ActividadcronogramaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['titulo', 'activo', 'fechacreacion']
    search_fields = ['titulo']

class ActividadtecnicaViewSet(ModelViewSet):
    queryset = Actividadtecnica.objects.order_by('pk')
    serializer_class = ActividadtecnicaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['idcomponente', 'estado', 'titulo', 'idcomponente__nombre']
    search_fields = ['titulo', 'idcomponente__nombre']




class PostulacionPropuestaViewSet(ModelViewSet):
    queryset = PostulacionPropuesta.objects.order_by('pk')
    serializer_class = PostulacionPropuestaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['idproyecto', 'titulo', 'idproyecto__nombre']
    search_fields = ['titulo', 'idproyecto__nombre']

class UserCursoViewSet(ModelViewSet):
    queryset = UserCurso.objects.order_by('pk')
    serializer_class = UserCursoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['iduser', 'idcurso', 'iduser__username', 'idcurso__nombre']
    search_fields = ['iduser__username', 'idcurso__nombre']

class UsuarioDesafioViewSet(ModelViewSet):
    queryset = UsuarioDesafio.objects.order_by('pk')
    serializer_class = UsuarioDesafioSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['iduser', 'idproyecto', 'iduser__username', 'idproyecto__nombre']
    search_fields = ['iduser__username', 'idproyecto__nombre']