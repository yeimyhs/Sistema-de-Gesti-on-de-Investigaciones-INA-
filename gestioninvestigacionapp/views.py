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


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

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


class ArchivoViewSet(ModelViewSet):
    queryset = Archivo.objects.order_by('pk')
    serializer_class = ArchivoSerializer


class ArchivoActividadesViewSet(ModelViewSet):
    queryset = ArchivoActividades.objects.order_by('pk')
    serializer_class = ArchivoActividadesSerializer


class ArchivoPostulacionesViewSet(ModelViewSet):
    queryset = ArchivoPostulaciones.objects.order_by('pk')
    serializer_class = ArchivoPostulacionesSerializer


class ComponenteViewSet(ModelViewSet):
    queryset = Componente.objects.order_by('pk')
    serializer_class = ComponenteSerializer


class ConvocatoriaViewSet(ModelViewSet):
    queryset = Convocatoria.objects.order_by('pk')
    serializer_class = ConvocatoriaSerializer


class CursoViewSet(ModelViewSet):
    queryset = Curso.objects.order_by('pk')
    serializer_class = CursoSerializer


class DepartamentoViewSet(ModelViewSet):
    queryset = Departamento.objects.order_by('pk')
    serializer_class = DepartamentoSerializer


class DesafioViewSet(ModelViewSet):
    queryset = Desafio.objects.order_by('pk')
    serializer_class = DesafioSerializer


class EntregableViewSet(ModelViewSet):
    queryset = Entregable.objects.order_by('pk')
    serializer_class = EntregableSerializer


class EvaluacionViewSet(ModelViewSet):
    queryset = Evaluacion.objects.order_by('pk')
    serializer_class = EvaluacionSerializer


class NotificcionesViewSet(ModelViewSet):
    queryset = Notificciones.objects.order_by('pk')
    serializer_class = NotificcionesSerializer


class PlantesisViewSet(ModelViewSet):
    queryset = Plantesis.objects.order_by('pk')
    serializer_class = PlantesisSerializer


class PostulanteViewSet(ModelViewSet):
    queryset = Postulante.objects.order_by('pk')
    serializer_class = PostulanteSerializer


class PresupuestoViewSet(ModelViewSet):
    queryset = Presupuesto.objects.order_by('pk')
    serializer_class = PresupuestoSerializer


class ReporteViewSet(ModelViewSet):
    queryset = Reporte.objects.order_by('pk')
    serializer_class = ReporteSerializer


class RetroalimentacionViewSet(ModelViewSet):
    queryset = Retroalimentacion.objects.order_by('pk')
    serializer_class = RetroalimentacionSerializer


class RetroalimentacionacttecnicaViewSet(ModelViewSet):
    queryset = Retroalimentacionacttecnica.objects.order_by('pk')
    serializer_class = RetroalimentacionacttecnicaSerializer


class RubricaViewSet(ModelViewSet):
    queryset = Rubrica.objects.order_by('pk')
    serializer_class = RubricaSerializer


class UserViewSet(ModelViewSet):
    queryset = CustomUser.objects.order_by('pk')
    serializer_class = UserSerializer


class ActividadcronogramaViewSet(ModelViewSet):
    queryset = Actividadcronograma.objects.order_by('pk')
    serializer_class = ActividadcronogramaSerializer


class ActividadtecnicaViewSet(ModelViewSet):
    queryset = Actividadtecnica.objects.order_by('pk')
    serializer_class = ActividadtecnicaSerializer



class PostulacionPropuestaViewSet(ModelViewSet):
    queryset = PostulacionPropuesta.objects.order_by('pk')
    serializer_class = PostulacionPropuestaSerializer


class UserCursoViewSet(ModelViewSet):
    queryset = UserCurso.objects.order_by('pk')
    serializer_class = UserCursoSerializer


class UsuarioDesafioViewSet(ModelViewSet):
    queryset = UsuarioDesafio.objects.order_by('pk')
    serializer_class = UsuarioDesafioSerializer
