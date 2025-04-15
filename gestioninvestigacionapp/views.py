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


from rest_framework import viewsets

class SoftDeleteViewSet(viewsets.ModelViewSet):
    """
    ViewSet base que implementa borrado lógico en vez de eliminación real.
    """
    def destroy(self, request, *args, **kwargs):
        """En lugar de eliminar, marca el objeto como eliminado."""
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Registro marcado como eliminado."}, status=status.HTTP_204_NO_CONTENT)
    
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        user_data = serializer.data
        user_data['id'] = user.pk  # Agregar el id al nivel de los datos del usuario

        return Response({
            "user": user_data,  # Ahora incluye el id en el mismo nivel que el resto de datos del usuario
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
        
class ConfiguracionViewSet(SoftDeleteViewSet):
    queryset = Configuracion.objects.order_by('pk')
    serializer_class = ConfiguracionSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['email', 'telefono', 'direccion']
    search_fields = ['email', 'telefono', 'direccion']
  
  
class ActividadViewSet(SoftDeleteViewSet):
    queryset = Actividad.objects.order_by('pk')
    serializer_class = ActividadSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['idactividad', 'tipo', 'fechaentrega', 'fechacreacion', 'eliminado', 'estado', 'idproyecto', 'idproyecto__titulo']
    search_fields = ['titulo', 'descripcion', 'idproyecto__titulo']
    
class ArchivoViewSet(SoftDeleteViewSet):
    queryset = Archivo.objects.order_by('pk')
    serializer_class = ArchivoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['idarchivo', 'eliminado', 'fechacreacion', 'idconvocatoria', 'idconvocatoria__titulo', 'idproyecto', 'idproyecto__titulo']
    search_fields = ['nombre', 'idconvocatoria__titulo', 'idproyecto__titulo']
    
class ArchivoActividadesViewSet(SoftDeleteViewSet):
    queryset = ArchivoActividades.objects.order_by('pk')
    serializer_class = ArchivoActividadesSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['idarchivo', 'eliminado', 'fechacreacion', 'idactividad', 'idactividad__titulo']
    search_fields = ['nombre', 'idactividad__titulo']


class ComponenteViewSet(SoftDeleteViewSet):
    queryset = Componente.objects.order_by('pk')
    serializer_class = ComponenteSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['idcomponente', 'numero', 'iddatostecnicos', 'iddatostecnicos__descripcion']
    search_fields = ['iddatostecnicos__descripcion']

class DatosTecnicosViewSet(SoftDeleteViewSet):
    queryset = DatosTecnicos.objects.order_by('pk')
    serializer_class = DatosTecnicosSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['descripcion']
    search_fields = ['descripcion']
    
    
class ConvocatoriaViewSet(SoftDeleteViewSet):
    queryset = Convocatoria.objects.order_by('pk')
    serializer_class = ConvocatoriaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['idconvocatoria', 'eliminado', 'estado', 'fechacreacion', 'iddepartamento']
    search_fields = ['titulo', 'descripcion', 'objetivogeneral']

class CursoViewSet(SoftDeleteViewSet):
    queryset = Curso.objects.order_by('pk')
    serializer_class = CursoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['idcurso', 'anioacademico', 'semestre', 'eliminado', 'estado', 'iddepartamento', 'iddepartamento__nombre', "nivel"]
    search_fields = ['titulo', 'iddepartamento__nombre']

class DepartamentoViewSet(SoftDeleteViewSet):
    queryset = Departamento.objects.order_by('pk')
    serializer_class = DepartamentoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['iddepartamento', 'estado', 'eliminado', 'fechacreacion']
    search_fields = ['nombre', 'lugar', 'email', 'director']

    @action(detail=False, methods=['get'], url_path='mis-departamentos/(?P<iduser>\d+)')
    def mis_departamentos(self, request, iduser=None):
        """Obtiene los departamentos donde el usuario con iduser es director."""
        departamentos = Departamento.objects.filter(director=iduser, eliminado=False)
        serializer = self.get_serializer(departamentos, many=True)
        return Response(serializer.data)
    
class DesafioViewSet(SoftDeleteViewSet):
    queryset = Desafio.objects.order_by('pk')
    serializer_class = DesafioSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['idproyecto', 'estado', 'eliminado', 'fechacreacion', 'idconvocatoria', 'idconvocatoria__titulo']
    search_fields = ['titulo', 'descripcion', 'idconvocatoria__titulo']


class EntregableViewSet(SoftDeleteViewSet):
    queryset = Entregable.objects.order_by('pk')
    serializer_class = EntregableSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['idactividadtecnica', 'comentario', 'idactividadtecnica__titulo']
    search_fields = ['comentario', 'idactividadtecnica__titulo']

class EvaluacionViewSet(SoftDeleteViewSet):
    queryset = Evaluacion.objects.order_by('pk')
    serializer_class = EvaluacionSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['idevaluacion', 'idplanformacion', 'idplanformacion__titulo']
    search_fields = ['comentario', 'idplanformacion__titulo']

class NotificcionesViewSet(SoftDeleteViewSet):
    queryset = Notificciones.objects.order_by('pk')
    serializer_class = NotificcionesSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['idnotificacion', 'eliminado', 'fechacreacion', 'iduser']
    search_fields = ['titulo', 'descripcion']


class PlantesisViewSet(SoftDeleteViewSet):
    queryset = Plantesis.objects.order_by('pk')
    serializer_class = PlantesisSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = [ 'titulo','justificacion','abstract' ]
    search_fields = ['titulo', 'abstract','justificacion']


class PostulanteViewSet(SoftDeleteViewSet):
    queryset = Postulante.objects.order_by('pk')
    serializer_class = PostulanteSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['iduser', 'eliminado', 'fechacreacion', 'idpostulacionpropuesta']
    search_fields = ['nombres', 'apellidos', 'email', 'institucion']


class PresupuestoViewSet(SoftDeleteViewSet):
    queryset = Presupuesto.objects.order_by('pk')
    serializer_class = PresupuestoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['idpresupuesto', 'idpostulacionpropuesta','monto','partida']
    search_fields = ['monto','partida']


class ReporteViewSet(SoftDeleteViewSet):
    queryset = Reporte.objects.order_by('pk')
    serializer_class = ReporteSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['idreporte', 'evaluacionnota', 'idactividad','idactividad__titulo']
    search_fields = ['idactividad__titulo']



class RetroalimentacionViewSet(SoftDeleteViewSet):
    queryset = Retroalimentacion.objects.order_by('pk')
    serializer_class = RetroalimentacionSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['idreporte', 'comentario']
    search_fields = ['comentario']


class RetroalimentacionacttecnicaViewSet(SoftDeleteViewSet):
    queryset = Retroalimentacionacttecnica.objects.order_by('pk')
    serializer_class = RetroalimentacionacttecnicaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['identregable', 'comentario']
    search_fields = ['comentario']

class RubricaViewSet(SoftDeleteViewSet):
    queryset = Rubrica.objects.order_by('pk')
    serializer_class = RubricaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['descripcion']
    search_fields = ['descripcion']
    
class CriterioViewSet(SoftDeleteViewSet):
    queryset = Criterio.objects.order_by('pk')
    serializer_class = CriterioSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['titulo','descripcion',"peso",'puntaje','idrubrica'  ]
    search_fields = ['titulo','descripcion',"peso",'puntaje' ]

class UserViewSet(SoftDeleteViewSet):
    queryset = CustomUser.objects.prefetch_related('usuariorolsistema_set__idrol').all().order_by('pk')
    serializer_class = CustomUserSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = [    'id', 'nombres', 'apellidos', 'telefono', 'eliminado',    'instituto', 'pais', 'ciudad', 'email', 'email_verified_at']
    
    search_fields = [
        'nombres', 'apellidos', 'telefono', 
        'instituto', 'pais', 'ciudad', 'email'
    ]
class ActividadcronogramaViewSet(SoftDeleteViewSet):
    queryset = Actividadcronograma.objects.order_by('pk')
    serializer_class = ActividadcronogramaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['titulo', 'eliminado', 'fechacreacion']
    search_fields = ['titulo']

class ActividadtecnicaViewSet(SoftDeleteViewSet):
    queryset = Actividadtecnica.objects.order_by('pk')
    serializer_class = ActividadtecnicaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['idcomponente', 'estado', 'titulo', 'idcomponente__numero']
    search_fields = ['titulo', 'idcomponente__numero']




class PostulacionPropuestaViewSet(SoftDeleteViewSet):
    queryset = PostulacionPropuesta.objects.prefetch_related("idproyecto__idconvocatoria", "iduser",'postulante_set').order_by('pk')
    serializer_class = PostulacionPropuestaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['idproyecto', 'titulo', 'idproyecto__titulo','aceptado','iduser','iduser__nombres','iduser__email','aceptado','practico','rentable','pionero','total','idproyecto__idconvocatoria', 'estado']
    search_fields = ['titulo', 'idproyecto__titulo','iduser__nombres']
    @action(detail=False, methods=['get'], url_path='detalle-convocatoria-listado')
    def detalle_convocatoria(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = PostulacionPropuestaConvocatoriaDetalleSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = PostulacionPropuestaConvocatoriaDetalleSerializer(queryset, many=True)
        return Response(serializer.data)

    
class UserCursoViewSet(SoftDeleteViewSet):
    queryset = UserCurso.objects.order_by('pk')
    serializer_class = UserCursoDetalleUserSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['iduser', 'idcurso', 'iduser__nombres', 'idcurso__titulo', 'rol']
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
    
    @action(detail=False, methods=["post"], url_path="matricular_estudiantes")
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

        # Verificar que los estudiantes no estén ya matriculados en el curso
        matriculados = UserCurso.objects.filter(idcurso=curso, iduser__in=idusers)
        matriculados_ids = {uc.iduser.id for uc in matriculados}

        if len(matriculados_ids) > 0:
            return Response({"error": f"Los siguientes usuarios ya están matriculados: {', '.join(map(str, matriculados_ids))}"}, status=status.HTTP_400_BAD_REQUEST)

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
    
    
    @action(detail=False, methods=["post"], url_path="desmatricular_estudiantes")
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
            return Response({"error": "Uno o varios usuarios no existen."}, status=status.HTTP_400_BAD_REQUEST)

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
    
    @action(detail=False, methods=["patch"], url_path="actualizar_matriculados")
    def actualizar_matriculados(self, request):

        """ Servicio para actualizar la lista de estudiantes matriculados en un curso y los desafíos asociados """
        data = request.data
        idcurso = data.get("idcurso")
        nuevos_idusers = set(data.get("idusers", []))  # Matricular los usuarios
        nuevos_desafios_ids = set(data.get("desafios_ids", []))  # Nuevos desafíos para el curso

        # Validar que el curso existe
        try:
            curso = Curso.objects.get(pk=idcurso)
        except Curso.DoesNotExist:
            return Response({"error": "El curso no existe."}, status=status.HTTP_400_BAD_REQUEST)

        # Actualización de matrícula de estudiantes
        matriculados_actuales = UserCurso.objects.filter(idcurso=curso, rol=7)
        matriculados_ids = {uc.iduser.id for uc in matriculados_actuales}

        ids_a_eliminar = matriculados_ids - nuevos_idusers
        ids_a_agregar = nuevos_idusers - matriculados_ids

        # Validar que los usuarios a agregar existan
        usuarios_a_agregar = CustomUser.objects.filter(id__in=ids_a_agregar)
        if len(usuarios_a_agregar) != len(ids_a_agregar):
            return Response({"error": "Uno o más usuarios a agregar no existen."}, status=status.HTTP_400_BAD_REQUEST)

        # Actualizar matrícula de estudiantes
        try:
            with transaction.atomic():
                # Eliminar los registros de usuarios que ya no deberían estar matriculados
                UserCurso.objects.filter(idcurso=curso, rol=7, iduser__id__in=ids_a_eliminar).delete()

                # Agregar nuevos usuarios
                nuevos_registros = [UserCurso(iduser=user, idcurso=curso, rol=7) for user in usuarios_a_agregar]
                UserCurso.objects.bulk_create(nuevos_registros)

        except Exception as e:
            return Response({"error": f"Error al actualizar matriculados: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Actualización de desafíos asociados al curso
        desafios_actuales = CursoDesafio.objects.filter(idcurso=curso).values_list('idproyecto', flat=True)
        desafios_actuales_ids = set(desafios_actuales)

        # Determinar los desafíos a eliminar (los que están asociados pero no están en la nueva lista)
        desafios_a_eliminar = desafios_actuales_ids - nuevos_desafios_ids
        # Determinar los desafíos a agregar (los que están en la nueva lista pero no estaban asociados)
        desafios_a_agregar = nuevos_desafios_ids - desafios_actuales_ids

        # Actualizar desafíos asociados al curso
        try:
            with transaction.atomic():
                # Eliminar los registros de desafíos que ya no deberían estar asociados
                CursoDesafio.objects.filter(idcurso=curso, idproyecto__in=desafios_a_eliminar).delete()

                # Agregar nuevos desafíos
                nuevos_registros_desafios = [CursoDesafio(idcurso=curso, idproyecto=Desafio.objects.get(id=id)) for id in desafios_a_agregar]
                CursoDesafio.objects.bulk_create(nuevos_registros_desafios)

        except Exception as e:
            return Response({"error": f"Error al actualizar desafíos: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

        # Obtener la lista actualizada de desafíos asociados al curso
        desafios_actualizados = CursoDesafio.objects.filter(idcurso=curso).select_related('idproyecto')
        lista_desafios = [
            {
                "id": cd.idproyecto.id,
                "titulo": cd.idproyecto.titulo
            }
            for cd in desafios_actualizados
        ]

        return Response({
            "message": "Matrícula y desafíos actualizados correctamente.",
            "matriculados": lista_matriculados,
            "desafios": lista_desafios
        }, status=status.HTTP_200_OK)
        
        
    def get_serializer_class(self):
        """Permite cambiar el serializador según la acción."""
        if self.action == 'cursos_detalle':
            return UserCursoCursoDetalleSerializer
        elif self.action == 'detallecompleto':
            return UserCursoFulldetalleSerializer
        return super().get_serializer_class()

    @action(detail=False, methods=['get'], url_path='detallecursos/(?P<iduser>\d+)')
    def cursos_detalle(self, request, iduser=None):
        """Obtiene cursos con detalles para un usuario específico con filtros."""
        queryset = UserCurso.objects.filter(iduser=iduser)
        
        # APLICAR FILTROS MANUALMENTE
        queryset = self.filter_queryset(queryset)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='detallecompleto')
    def detallecompleto(self, request):
        queryset = UserCurso.objects.select_related('iduser', 'idcurso').all()

        # 💡 Limpieza de parámetros vacíos
        query_params = {k: v for k, v in request.GET.items() if v}

        # ⚙️ Clonamos request con los parámetros limpios
        request._request.GET = query_params  # Esto es un truco para filtros personalizados

        # 🔍 Aplicamos filtros
        for backend in (DjangoFilterBackend(), filters.SearchFilter(), filters.OrderingFilter()):
            queryset = backend.filter_queryset(request, queryset, self)

        # Paginación y serialización
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = UserCursoFulldetalleSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = UserCursoFulldetalleSerializer(queryset, many=True)
        return Response(serializer.data)
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from django_filters import filters as django_filters
from rest_framework import filters

# Define un filtro personalizado
class CursoDesafioFilter(FilterSet):
    idcurso__in = django_filters.BaseInFilter(field_name='idcurso')
    
    class Meta:
        model = CursoDesafio
        fields = ['idproyecto', 'idcurso', 'iddatostecnicos', 'idplanformacion', 'idcurso__titulo']

class CursoDesafioViewSet(SoftDeleteViewSet):
    queryset = CursoDesafio.objects.order_by('pk')
    serializer_class = CursoDesafioSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_class = CursoDesafioFilter  # Usar la clase de filtro personalizada
    search_fields = ['idproyecto__titulo', 'idcurso__titulo']
    
    
    
    
class UsuarioDesafioViewSet(SoftDeleteViewSet):
    queryset = UsuarioDesafio.objects.order_by('pk')
    serializer_class = UsuarioDesafioSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['iduser', 'idproyecto', 'iduser_id__nombres', 'idproyecto__titulo']
    search_fields = ['iduser__nombres', 'idproyecto__titulo']

    def get_serializer_class(self):
        """Permite cambiar el serializador según la acción."""
        if self.action == 'desafio_detalle':
            return UsuarioDesafioDesafioDetalleSerializer
        return super().get_serializer_class()

    @action(detail=False, methods=['get'], url_path='desafio_detalle/(?P<iduser>\d+)')
    def desafio_detalle(self, request, iduser=None):
        """Obtiene cursos con detalles para un usuario específico con filtros."""
        queryset = UsuarioDesafio.objects.filter(iduser=iduser)
        
        # APLICAR FILTROS MANUALMENTE
        queryset = self.filter_queryset(queryset)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data) 
    
class EstadoViewSet(SoftDeleteViewSet):
    queryset = Estado.objects.order_by('pk')
    serializer_class = EstadoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['tipodashboard','valor', 'clave', 'descripcion', 'identificador_tabla', 'nombre_tabla']
    search_fields = ['valor', 'clave', 'descripcion', 'identificador_tabla', 'nombre_tabla']
    
    
class ubigeoPaisViewSet(SoftDeleteViewSet):
    queryset = ubigeoPais.objects.order_by('pk')
    serializer_class = ubigeoPaisSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['idpais', 'nombre']
    search_fields = ['nombre']



class ubigeoDepartamentoViewSet(SoftDeleteViewSet):
    queryset = ubigeoDepartamento.objects.order_by('pk')
    serializer_class = ubigeoDepartamentoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['iddepartamento', 'nombre']
    search_fields = ['nombre']


class ubigeoProvinciaViewSet(SoftDeleteViewSet):
    queryset = ubigeoProvincia.objects.order_by('pk')
    serializer_class = ubigeoProvinciaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['idprovincia', 'nombre', 'iddepartamento']
    search_fields = ['nombre']


class ubigeoDistritoViewSet(SoftDeleteViewSet):
    queryset = ubigeoDistrito.objects.order_by('pk')
    serializer_class = ubigeoDistritoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['idciudad', 'nombre', 'idprovincia']
    search_fields = ['nombre']

from django.db.models import Count, Min

class UsuarioRolSistemaViewSet(SoftDeleteViewSet):
    queryset = UsuarioRolSistema.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    serializer_class = UsuarioRolSistemaSerializer
    filterset_fields = ['iduser','idrol']
    search_fields = ['idrol', 'iduser']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Verificar si se solicita filtrar combinaciones únicas
        unique = self.request.query_params.get('unique', None)
        
        if unique and unique.lower() == 'true':
            # Obtener solo las primeras ocurrencias de cada combinación iduser-idrol
            unique_combinations = {}
            
            # Aplicamos los filtros primero para respetar otros parámetros de consulta
            filtered_queryset = self.filter_queryset(queryset)
            
            # Usamos un conjunto para rastrear combinaciones ya vistas
            seen_combinations = set()
            ids_to_keep = []
            
            for item in filtered_queryset:
                # Creamos una clave única para la combinación
                combo_key = (str(item.iduser_id), str(item.idrol_id))
                
                if combo_key not in seen_combinations:
                    seen_combinations.add(combo_key)
                    ids_to_keep.append(item.id)
            
            # Filtramos el queryset original con los IDs a mantener
            return UsuarioRolSistema.objects.filter(id__in=ids_to_keep)
            
        return queryset
    
    @action(detail=False, methods=['get'])
    def unique_combinations(self, request):
        """Endpoint para obtener solo registros con combinaciones únicas de usuario y rol"""
        queryset = self.get_queryset()
        # Aplicamos los filtros normales
        queryset = self.filter_queryset(queryset)
        
        # Identificamos combinaciones únicas y nos quedamos con el ID menor de cada una
        unique_ids = queryset.values('iduser', 'idrol').annotate(min_id=Min('id')).values_list('min_id', flat=True)
        
        # Filtramos el queryset para incluir solo estos IDs
        filtered_queryset = UsuarioRolSistema.objects.filter(id__in=unique_ids)
        
        # Serializamos y devolvemos el resultado
        page = self.paginate_queryset(filtered_queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = self.get_serializer(filtered_queryset, many=True)
        return Response(serializer.data)
    
class EmpresaViewSet(SoftDeleteViewSet):
    queryset = Empresa.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    serializer_class = EmpresaSerializer
    filterset_fields = ['descripcion','nombre', 'publico', 'estado']
    search_fields = ['descripcion','nombre', 'publico', 'estado']
    
    
class HistoriaexitoViewSet(SoftDeleteViewSet):
    queryset = Historiaexito.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    serializer_class = HistoriaexitoSerializer
    filterset_fields = ['historia','nombre', 'cargo', 'estado']
    search_fields = ['historia','nombre', 'cargo', 'estado']
    
    

class RolViewSet(SoftDeleteViewSet):
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
