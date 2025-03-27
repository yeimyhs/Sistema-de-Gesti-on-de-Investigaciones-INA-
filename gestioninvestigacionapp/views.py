from rest_framework.viewsets import ModelViewSet
from gestioninvestigacionapp.serializers import ActividadSerializer, ArchivoSerializer, ArchivoActividadesSerializer, ComponenteSerializer, ConvocatoriaSerializer, CursoSerializer, DepartamentoSerializer, DesafioSerializer, EntregableSerializer, EvaluacionSerializer, NotificcionesSerializer, PlantesisSerializer, PostulanteSerializer, PresupuestoSerializer, ReporteSerializer, RetroalimentacionSerializer, RetroalimentacionacttecnicaSerializer, RubricaSerializer, ActividadcronogramaSerializer, ActividadtecnicaSerializer, PostulacionPropuestaSerializer, UserCursoSerializer, UsuarioDesafioSerializer
from gestioninvestigacionapp.serializers import *
from gestioninvestigacionapp.models import Actividad, Archivo, ArchivoActividades, Componente, Convocatoria, Curso, Departamento, Desafio, Entregable, Evaluacion, Notificciones, Plantesis, Postulante, Presupuesto, Reporte, Retroalimentacion, Retroalimentacionacttecnica, Rubrica, Actividadcronograma, Actividadtecnica, PostulacionPropuesta, UserCurso, UsuarioDesafio
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


from django.db import transaction
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status



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
    filterset_fields = ['idconvocatoria', 'eliminado', 'estado', 'fechacreacion', 'iddepartamento']
    search_fields = ['titulo', 'descripcion', 'objetivogeneral']

class CursoViewSet(ModelViewSet):
    queryset = Curso.objects.order_by('pk')
    serializer_class = CursoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['idcurso', 'anioacademico', 'semestre', 'eliminado', 'estado', 'iddepartamento', 'iddepartamento__nombre', "nivel"]
    search_fields = ['titulo', 'iddepartamento__nombre']

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
    search_fields = ['titulo', 'descripcion', 'idconvocatoria__titulo']


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
    filterset_fields = ['iduser', 'eliminado', 'fechacreacion', 'idpostulacionpropuesta']
    search_fields = ['nombres', 'apellidos', 'email', 'institucion']


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
    queryset = PostulacionPropuesta.objects.prefetch_related("idproyecto__idconvocatoria", "iduser",'postulante_set').order_by('pk')
    serializer_class = PostulacionPropuestaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['idproyecto', 'titulo', 'idproyecto__titulo','aceptado','iduser','iduser__nombres','iduser__email','aceptado','practico','rentable','pionero','total','idproyecto__idconvocatoria']
    search_fields = ['titulo', 'idproyecto__titulo','iduser__nombres']

class UserCursoViewSet(ModelViewSet):
    queryset = UserCurso.objects.order_by('pk')
    serializer_class = UserCursoDetalleUserSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['iduser', 'idcurso', 'iduser__nombres', 'idcurso__titulo']
    search_fields = ['iduser__nombres', 'idcurso__titulo']
    
    def create(self, request, *args, **kwargs):
        """ Sobrescribe el método de creación para agregar automáticamente un registro en UsuarioRolSistema. """
        with transaction.atomic():
            # Crear el registro en UserCurso
            response = super().create(request, *args, **kwargs)
            
            # Obtener los datos creados
            usercurso = UserCurso.objects.get(pk=response.data['id'])
            iduser = usercurso.iduser
            idrol = usercurso.rol  # Usamos el rol recibido en la solicitud

            # Verificar si la combinación (iduser, idrol) ya existe en UsuarioRolSistema
            UsuarioRolSistema.objects.create(iduser=iduser, idrol_id=idrol)

        return response
    
    @action(detail=False, methods=["post"])
    def matricular_estudiantes(self, request):
        """ Servicio para matricular múltiples estudiantes en un curso. """
        data = request.data
        idcurso = data.get("idcurso")
        idusers = data.get("idusers", [])  # Lista de IDs de usuarios

        # Validar que el curso existe
        try:
            curso = Curso.objects.get(pk=idcurso)
        except Curso.DoesNotExist:
            return Response({"error": "El curso no existe."}, status=status.HTTP_400_BAD_REQUEST)

        # Validar que los usuarios existen
        usuarios = CustomUser.objects.filter(id__in=idusers)
        if usuarios.count() != len(idusers):
            return Response({"error": "Uno o más usuarios no existen."}, status=status.HTTP_400_BAD_REQUEST)

        # Transacción para garantizar que todas las inserciones sean atómicas
        try:
            with transaction.atomic():
                registros = [
                    UserCurso(iduser=user, idcurso=curso, rol=7)
                    for user in usuarios
                ]
                UserCurso.objects.bulk_create(registros)
        except Exception as e:
            return Response({"error": f"Error al matricular: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message": "Estudiantes matriculados exitosamente."}, status=status.HTTP_201_CREATED)
    @action(detail=False, methods=["post"])
    def desmatricular_estudiantes(self, request):
        """ Servicio para desmatricular múltiples estudiantes de un curso. """
        data = request.data
        idcurso = data.get("idcurso")
        idusers = data.get("idusers", [])  # Lista de IDs de usuarios

        # Validar que el curso existe
        try:
            curso = Curso.objects.get(pk=idcurso)
        except Curso.DoesNotExist:
            return Response({"error": "El curso no existe."}, status=status.HTTP_400_BAD_REQUEST)

        # Validar que los usuarios existen
        usuarios = CustomUser.objects.filter(id__in=idusers)
        if usuarios.count() != len(idusers):
            return Response({"error": "Uno o más usuarios no existen."}, status=status.HTTP_400_BAD_REQUEST)

        # Intentar eliminar los registros de matrícula
        try:
            with transaction.atomic():
                eliminados, _ = UserCurso.objects.filter(
                    idcurso=curso, iduser__in=usuarios, rol=7
                ).delete()
        except Exception as e:
            return Response({"error": f"Error al desmatricular: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if eliminados == 0:
            return Response({"message": "No se encontraron registros para eliminar."}, status=status.HTTP_404_NOT_FOUND)

        return Response({"message": f"{eliminados} estudiantes desmatriculados exitosamente."}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=["patch"])
    def actualizar_matriculados(self, request):
        """ Servicio para actualizar la lista de estudiantes matriculados en un curso y devolver la lista actualizada. """
        data = request.data
        idcurso = data.get("idcurso")
        nuevos_idusers = set(data.get("idusers", []))  # Convertir en conjunto para comparación rápida

        # Validar que el curso existe
        try:
            curso = Curso.objects.get(pk=idcurso)
        except Curso.DoesNotExist:
            return Response({"error": "El curso no existe."}, status=status.HTTP_400_BAD_REQUEST)

        # Obtener la lista actual de matriculados en el curso con rol=7
        matriculados_actuales = UserCurso.objects.filter(idcurso=curso, rol=7)
        matriculados_ids = {uc.iduser.id for uc in matriculados_actuales}

        # Determinar los usuarios a eliminar (los que están matriculados pero no en la nueva lista)
        ids_a_eliminar = matriculados_ids - nuevos_idusers
        # Determinar los usuarios a agregar (los que están en la nueva lista pero no estaban matriculados)
        ids_a_agregar = nuevos_idusers - matriculados_ids

        # Validar que los usuarios a agregar existan
        usuarios_a_agregar = CustomUser.objects.filter(id__in=ids_a_agregar)
        if len(usuarios_a_agregar) != len(ids_a_agregar):
            return Response({"error": "Uno o más usuarios a agregar no existen."}, status=status.HTTP_400_BAD_REQUEST)

        # Transacción para garantizar la consistencia
        try:
            with transaction.atomic():
                # Eliminar los registros de usuarios que ya no deberían estar matriculados
                UserCurso.objects.filter(idcurso=curso, rol=7, iduser__id__in=ids_a_eliminar).delete()

                # Agregar nuevos usuarios
                nuevos_registros = [UserCurso(iduser=user, idcurso=curso, rol=7) for user in usuarios_a_agregar]
                UserCurso.objects.bulk_create(nuevos_registros)

        except Exception as e:
            return Response({"error": f"Error al actualizar matriculados: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Obtener la lista actualizada de matriculados
        matriculados_actualizados = UserCurso.objects.filter(idcurso=curso, rol=7).select_related('iduser')
        lista_matriculados = [
            {
                "id": uc.iduser.id,
                "nombre": uc.iduser.nombres,
                "apellido": uc.iduser.apellidos,
                "email": uc.iduser.email
            }
            for uc in matriculados_actualizados
        ]

        return Response({
            "message": "Lista de matriculados actualizada correctamente.",
            "matriculados": lista_matriculados
        }, status=status.HTTP_200_OK)
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
    filterset_fields = ['tipodashboard','valor', 'clave', 'descripcion', 'identificador_tabla', 'nombre_tabla']
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
    filterset_fields = ['iduser','idrol']
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
    

# views.py
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

class ContactoAPIView(APIView):
    def post(self, request):
        subject = request.data.get("subject")  # Título del mensaje
        contenido = request.data.get("contenido")  # Cuerpo del mensaje
        #email_remitente = request.data.get("email")  # Email del usuario que envía

        # Validación rápida
        if not subject or not contenido :
            return Response({"error": "Todos los campos son obligatorios"}, status=status.HTTP_400_BAD_REQUEST)

        mensaje = f"{contenido}"

        try:
            send_mail(
                subject,
                mensaje,
                settings.DEFAULT_FROM_EMAIL,  # Remitente
                [settings.EMAIL_HOST_USER],  # Destinatario
                fail_silently=False,
            )
            return Response({"message": "Correo enviado correctamente"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
import uuid
from django.http import HttpResponse
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = CustomUser.objects.get(email=email)

            # Generar un token único
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            # Enviar correo
            scheme = request.scheme  # 'http' o 'https'
            host = request.get_host()  # Dominio del servidor
            reset_link = f"{scheme}://{host}/gestioninnovacion/password-reset?user_id={user.id}&token={token}"
            send_mail(
                "Recuperación de contraseña",
                f"Usa este enlace para restablecer tu contraseña: {reset_link}",
                "no-reply@example.com",
                [email]
            )
            return Response({"message": "Correo de recuperación enviado."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class PasswordResetView(APIView):
    def get(self, request):
        # Obtener parámetros de la URL
        user_id = request.query_params.get("user_id")
        token = request.query_params.get("token")

        # Validar los parámetros
        if not user_id or not token:
            return Response({"error": "Faltan parámetros en la URL."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        token_generator = PasswordResetTokenGenerator()
        if not token_generator.check_token(user, token):
            return Response({"error": "Token inválido o expirado."}, status=status.HTTP_400_BAD_REQUEST)

  # Incrustar el HTML básico
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Restablecer Contraseña</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 50px;
                    padding: 20px;
                    text-align: center;
                }}
                form {{
                    max-width: 400px;
                    margin: auto;
                }}
                input {{
                    width: 100%;
                    padding: 10px;
                    margin: 10px 0;
                    box-sizing: border-box;
                }}
                button {{
                    padding: 10px 20px;
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    cursor: pointer;
                }}
            </style>
        </head>
        <body>
            <h1>Restablecer Contraseña</h1>
            <form method="POST" action="/gestioninnovacion/login/">
                <input type="hidden" name="user_id" value="{user_id}">
                <input type="hidden" name="token" value="{token}">
                <label for="new_password">Nueva Contraseña:</label>
                <input type="password" id="new_password" name="new_password" required>
                <label for="confirm_password">Confirmar Contraseña:</label>
                <input type="password" id="confirm_password" name="confirm_password" required>
                <button type="submit">Restablecer</button>
            </form>
        </body>
        </html>
        """
        return HttpResponse(html_content, content_type="text/html")
        # Renderizar el formulario de restablecimiento de contraseña
        #return render(request, "password_reset_form.html", {"user_id": user_id, "token": token})
