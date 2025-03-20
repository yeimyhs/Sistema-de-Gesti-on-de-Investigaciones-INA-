from rest_framework.viewsets import ModelViewSet
from gestioninvestigacionapp.serializers import ActividadSerializer, ArchivoSerializer, ArchivoActividadesSerializer, ArchivoPostulacionesSerializer, ComponenteSerializer, ConvocatoriaSerializer, CursoSerializer, DepartamentoSerializer, DesafioSerializer, EntregableSerializer, EvaluacionSerializer, NotificcionesSerializer, PlantesisSerializer, PostulanteSerializer, PresupuestoSerializer, ReporteSerializer, RetroalimentacionSerializer, RetroalimentacionacttecnicaSerializer, RubricaSerializer, ActividadcronogramaSerializer, ActividadtecnicaSerializer, PostulacionPropuestaSerializer, UserCursoSerializer, UsuarioDesafioSerializer
from gestioninvestigacionapp.serializers import *
from gestioninvestigacionapp.models import Actividad, Archivo, ArchivoActividades, ArchivoPostulaciones, Componente, Convocatoria, Curso, Departamento, Desafio, Entregable, Evaluacion, Notificciones, Plantesis, Postulante, Presupuesto, Reporte, Retroalimentacion, Retroalimentacionacttecnica, Rubrica, Actividadcronograma, Actividadtecnica, PostulacionPropuesta, UserCurso, UsuarioDesafio
from .models import CustomUser
from .filters import *


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
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]

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

        # 🔥 Obtener el usuario autenticado desde el serializer
        user = serializer.validated_data["user"]

        # 🔥 Iniciar sesión manualmente (importante para Knox)
        login(request, user)

        # 🔥 Generar el token con Knox (esto es lo que fallaba antes)
        response = super(LoginView, self).post(request, format=None)

        # 🔥 Serializar información del usuario
        user_serializer = CustomUserSerializer(user)

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
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['idactividad', 'tipo', 'fechaentrega', 'fechacreacion', 'eliminado', 'estado', 'idproyecto', 'idproyecto__titulo']
    search_fields = ['titulo', 'descripcion', 'idproyecto__titulo']
    
class ArchivoViewSet(ModelViewSet):
    queryset = Archivo.objects.order_by('pk')
    serializer_class = ArchivoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['idarchivo', 'eliminado', 'fechacreacion', 'idconvocatoria', 'idconvocatoria__titulo', 'idproyecto', 'idproyecto__titulo']
    search_fields = ['nombre', 'idconvocatoria__titulo', 'idproyecto__titulo']
    
class ArchivoActividadesViewSet(ModelViewSet):
    queryset = ArchivoActividades.objects.order_by('pk')
    serializer_class = ArchivoActividadesSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['idarchivo', 'eliminado', 'fechacreacion', 'idactividad', 'idactividad__titulo']
    search_fields = ['nombre', 'idactividad__titulo']

class ArchivoPostulacionesViewSet(ModelViewSet):
    queryset = ArchivoPostulaciones.objects.order_by('pk')
    serializer_class = ArchivoPostulacionesSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['idarchivo', 'eliminado', 'fechacreacion', 'idconvocatoria', 'idproyecto', 'idproyecto__titulo']
    search_fields = ['nombre', 'idproyecto__titulo']

class ComponenteViewSet(ModelViewSet):
    queryset = Componente.objects.order_by('pk')
    serializer_class = ComponenteSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['idcomponente', 'numero', 'iddatostecnicos', 'iddatostecnicos__descripcion']
    search_fields = ['iddatostecnicos__descripcion']

class DatosTecnicosViewSet(ModelViewSet):
    queryset = DatosTecnicos.objects.order_by('pk')
    serializer_class = DatosTecnicosSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['descripcion']
    search_fields = ['descripcion']
    
    
class ConvocatoriaViewSet(ModelViewSet):
    queryset = Convocatoria.objects.order_by('pk')
    serializer_class = ConvocatoriaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['idconvocatoria', 'eliminado', 'estado', 'fechacreacion']
    search_fields = ['titulo', 'descripcion', 'objetivogeneral']

class CursoViewSet(ModelViewSet):
    queryset = Curso.objects.order_by('pk')
    serializer_class = CursoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['idcurso', 'anioacademico', 'semestre', 'eliminado', 'estado', 'iddepartamento', 'iddepartamento__nombre']
    search_fields = ['titulo', 'coordinador', 'iddepartamento__nombre']

class DepartamentoViewSet(ModelViewSet):
    queryset = Departamento.objects.order_by('pk')
    serializer_class = DepartamentoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['iddepartamento', 'estado', 'eliminado', 'fechacreacion']
    search_fields = ['nombre', 'lugar', 'email', 'director']


class DesafioViewSet(ModelViewSet):
    queryset = Desafio.objects.order_by('pk')
    serializer_class = DesafioSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['idproyecto', 'estado', 'eliminado', 'fechacreacion', 'idconvocatoria', 'idconvocatoria__titulo']
    search_fields = ['titulo', 'descripcion', 'idconvocatoria__titulo', '']


class EntregableViewSet(ModelViewSet):
    queryset = Entregable.objects.order_by('pk')
    serializer_class = EntregableSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['idactividadtecnica', 'comentario', 'idactividadtecnica__titulo']
    search_fields = ['comentario', 'idactividadtecnica__titulo']

class EvaluacionViewSet(ModelViewSet):
    queryset = Evaluacion.objects.order_by('pk')
    serializer_class = EvaluacionSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['idevaluacion', 'idplanformacion', 'idplanformacion__titulo']
    search_fields = ['comentario', 'idplanformacion__titulo']

class NotificcionesViewSet(ModelViewSet):
    queryset = Notificciones.objects.order_by('pk')
    serializer_class = NotificcionesSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['idnotificacion', 'eliminado', 'fechacreacion', 'iduser']
    search_fields = ['titulo', 'descripcion']


class PlantesisViewSet(ModelViewSet):
    queryset = Plantesis.objects.order_by('pk')
    serializer_class = PlantesisSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = [ 'titulo','justificacion','abstract' ]
    search_fields = ['titulo', 'abstract','justificacion']


class PostulanteViewSet(ModelViewSet):
    queryset = Postulante.objects.order_by('pk')
    serializer_class = PostulanteSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['iduser', 'eliminado', 'fechacreacion', 'idproyecto', 'idproyecto__titulo']
    search_fields = ['nombres', 'apellidos', 'email', 'institucion', 'idproyecto__titulo']


class PresupuestoViewSet(ModelViewSet):
    queryset = Presupuesto.objects.order_by('pk')
    serializer_class = PresupuestoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['idpresupuesto', 'idproyecto', 'idproyecto__titulo','monto','partida']
    search_fields = ['monto','partida', 'idproyecto__titulo']


class ReporteViewSet(ModelViewSet):
    queryset = Reporte.objects.order_by('pk')
    serializer_class = ReporteSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['idreporte', 'evaluacionnota', 'idactividad','idactividad__titulo']
    search_fields = ['idactividad__titulo']



class RetroalimentacionViewSet(ModelViewSet):
    queryset = Retroalimentacion.objects.order_by('pk')
    serializer_class = RetroalimentacionSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['idreporte', 'comentario']
    search_fields = ['comentario']


class RetroalimentacionacttecnicaViewSet(ModelViewSet):
    queryset = Retroalimentacionacttecnica.objects.order_by('pk')
    serializer_class = RetroalimentacionacttecnicaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['identregable', 'comentario']
    search_fields = ['comentario']

class RubricaViewSet(ModelViewSet):
    queryset = Rubrica.objects.order_by('pk')
    serializer_class = RubricaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['descripcion']
    search_fields = ['descripcion']
    
class CriterioViewSet(ModelViewSet):
    queryset = Criterio.objects.order_by('pk')
    serializer_class = CriterioSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['titulo','descripcion',"peso",'puntaje','idrubrica'  ]
    search_fields = ['titulo','descripcion',"peso",'puntaje' ]

class UserViewSet(ModelViewSet):
    queryset = CustomUser.objects.prefetch_related('usuariorolsistema_set__idrol').all().order_by('pk')
    serializer_class = CustomUserSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = [    'id', 'nombres', 'apellidos', 'telefono', 'eliminado',    'instituto', 'pais', 'ciudad', 'email', 'email_verified_at']
    
    search_fields = [
        'nombres', 'apellidos', 'telefono', 
        'instituto', 'pais', 'ciudad', 'email'
    ]
class ActividadcronogramaViewSet(ModelViewSet):
    queryset = Actividadcronograma.objects.order_by('pk')
    serializer_class = ActividadcronogramaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['titulo', 'eliminado', 'fechacreacion']
    search_fields = ['titulo']

class ActividadtecnicaViewSet(ModelViewSet):
    queryset = Actividadtecnica.objects.order_by('pk')
    serializer_class = ActividadtecnicaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['idcomponente', 'estado', 'titulo', 'idcomponente__numero']
    search_fields = ['titulo', 'idcomponente__numero']




class PostulacionPropuestaViewSet(ModelViewSet):
    queryset = PostulacionPropuesta.objects.order_by('pk')
    serializer_class = PostulacionPropuestaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['idproyecto', 'titulo', 'idproyecto__titulo']
    search_fields = ['titulo', 'idproyecto__titulo']

class UserCursoViewSet(ModelViewSet):
    queryset = UserCurso.objects.order_by('pk')
    serializer_class = UserCursoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['iduser', 'idcurso', 'iduser__nombres', 'idcurso__titulo']
    search_fields = ['iduser__nombres', 'idcurso__titulo']


class CursoDesafioViewSet(ModelViewSet):
    queryset = CursoDesafio.objects.order_by('pk')
    serializer_class = CursoDesafioSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['idproyecto', 'idcurso', 'iddatostecnicos','idplanformacion', 'idcurso__titulo']
    search_fields = ['idproyecto__titulo', 'idcurso__titulo']

class UsuarioDesafioViewSet(ModelViewSet):
    queryset = UsuarioDesafio.objects.order_by('pk')
    serializer_class = UsuarioDesafioSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['iduser', 'idproyecto', 'iduser_id__nombres', 'idproyecto__titulo']
    search_fields = ['iduser__nombres', 'idproyecto__titulo']
    
    
class EstadoViewSet(ModelViewSet):
    queryset = Estado.objects.order_by('pk')
    serializer_class = EstadoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['valor', 'clave', 'descripcion', 'identificador_tabla', 'nombre_tabla']
    search_fields = ['valor', 'clave', 'descripcion', 'identificador_tabla', 'nombre_tabla']
    
    
class ubigeoPaisViewSet(ModelViewSet):
    queryset = ubigeoPais.objects.order_by('pk')
    serializer_class = ubigeoPaisSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['idpais', 'nombre']
    search_fields = ['nombre']



class ubigeoDepartamentoViewSet(ModelViewSet):
    queryset = ubigeoDepartamento.objects.order_by('pk')
    serializer_class = ubigeoDepartamentoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['iddepartamento', 'nombre']
    search_fields = ['nombre']


class ubigeoProvinciaViewSet(ModelViewSet):
    queryset = ubigeoProvincia.objects.order_by('pk')
    serializer_class = ubigeoProvinciaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['idprovincia', 'nombre', 'iddepartamento']
    search_fields = ['nombre']


class ubigeoDistritoViewSet(ModelViewSet):
    queryset = ubigeoDistrito.objects.order_by('pk')
    serializer_class = ubigeoDistritoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['idciudad', 'nombre', 'idprovincia']
    search_fields = ['nombre']

class UsuarioRolSistemaViewSet(ModelViewSet):
    queryset = UsuarioRolSistema.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    serializer_class = UsuarioRolSistemaSerializer
    filterset_fields = []
    search_fields = ['idrol', 'iduser']
    
    

class RolViewSet(ModelViewSet):
    """
    API para gestionar los roles en el sistema.
    """
    queryset = Rol.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    serializer_class = RolSerializer
    filterset_fields = ['identificador_rol', 'titulo', 'descripcion']
    search_fields = ['identificador_rol', 'titulo', 'descripcion']
    
    