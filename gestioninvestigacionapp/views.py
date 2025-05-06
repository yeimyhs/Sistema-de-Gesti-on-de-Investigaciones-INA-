from django.db.models import Prefetch
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
    filterset_fields = ['idactividad','idcreador' , 'tipo', 'fechaentrega', 'fechacreacion', 'eliminado', 'estado', 'idproyecto', 'idproyecto__titulo']
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
    filterset_fields = ['descripcion','idcursodesafio']
    search_fields = ['descripcion']
    
from django_filters import rest_framework as dfilters
class NumberInFilter(dfilters.BaseInFilter, dfilters.NumberFilter):
    pass

class ConvocatoriaFilter(dfilters.FilterSet):
    estado__in = NumberInFilter(field_name='estado', lookup_expr='in')

    class Meta:
        model = Convocatoria
        fields = ['idconvocatoria', 'eliminado', 'estado', 'estado__in', 'fechacreacion', 'iddepartamento']
            
class ConvocatoriaViewSet(SoftDeleteViewSet):
    queryset = Convocatoria.objects.order_by('pk')
    serializer_class = ConvocatoriaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_class = ConvocatoriaFilter
    search_fields = ['titulo', 'descripcion', 'objetivogeneral']

class CursoViewSet(SoftDeleteViewSet):
    queryset = Curso.objects.order_by('pk')
    serializer_class = CursoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['idcurso', 'anioacademico', 'semestre', 'eliminado', 'estado', 'iddepartamento', 'iddepartamento__nombre', "nivel"]
    search_fields = ['titulo', 'iddepartamento__nombre']
    @action(detail=False, methods=['get'], url_path='cursos-por-departamento')
    def cursos_por_departamento(self, request):
        ids_param = request.query_params.get('departamentos', '')
        ids = [int(i) for i in ids_param.split(',') if i.isdigit()]
        
        if not ids:
            return Response({"error": "Debes enviar al menos un ID de departamento."}, status=400)

        queryset = self.filter_queryset(
            Curso.objects.filter(iddepartamento__pk__in=ids).select_related('iddepartamento')
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)  # Esto asegura que DRF use correctamente el serializador
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


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
    
    def get_queryset(self):
        return Desafio.objects.order_by('pk').prefetch_related(
            Prefetch(
                'usuariodesafio_set',
                queryset=UsuarioDesafio.objects.select_related('iduser').filter(eliminado=0),
                to_attr='usuarios_desafio_prefetch'
            )
        )
    @action(detail=False, methods=['get'], url_path='desafios-por-usuario')
    def desafios_por_usuario(self, request):
        iduser = request.query_params.get('iduser')
        if not iduser or not iduser.isdigit():
            return Response({"error": "ID de usuario inválido."}, status=400)

        try:
            usuario = User.objects.get(pk=iduser)
        except User.DoesNotExist:
            return Response({"error": "Usuario no encontrado."}, status=404)

        relaciones_desafio = UsuarioDesafio.objects.filter(
            iduser=iduser
        ).select_related('idproyecto', 'iduser')

        relaciones_curso = UserCurso.objects.filter(iduser=iduser).select_related('idcurso')

        serializer = DesafiosUsuarioConCursoSerializer({
            "usuario": usuario,
            "relaciones_desafio": relaciones_desafio,
            "relaciones_curso": relaciones_curso,
        })

        return Response(serializer.data)

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
    filterset_fields = ['idevaluacion', 'idplanformacion', 'idplanformacion__titulo', 'idrubrica', 'iduserevaluador']
    search_fields = ['comentario', 'idplanformacion__titulo']
    def get_queryset(self):
        return Evaluacion.objects.select_related(
            'idrubrica'  # FK directa a Rubrica
        ).prefetch_related(
            # Cargar criterios evaluados con su criterio relacionado
            Prefetch(
                'evaluacioncriterio_set',
                queryset=EvaluacionCriterio.objects.select_related('idcriterio')
            ),
            # Cargar los criterios de la rúbrica (si la rúbrica tiene M2M o FK a criterio)
            Prefetch(
                'idrubrica__criterio_set',  # Esto depende de tu modelo Rubrica
                queryset=Criterio.objects.all()
            )
        )
class EvaluacionCriterioViewSet(SoftDeleteViewSet):
    queryset = EvaluacionCriterio.objects.order_by('pk')
    serializer_class = EvaluacionCriterioSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['idevaluacion', 'idcriterio', 'puntaje']
    search_fields = [ 'idcriterio__titulo']


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
    filterset_fields = ['idactividad', 'comentario','idusercreador']
    search_fields = ['comentario']


class RetroalimentacionacttecnicaViewSet(SoftDeleteViewSet):
    queryset = Retroalimentacionacttecnica.objects.order_by('pk')
    serializer_class = RetroalimentacionacttecnicaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['identregable', 'comentario','idusercreador']
    search_fields = ['comentario']

class RubricaViewSet(SoftDeleteViewSet):
    queryset = Rubrica.objects.order_by('pk')
    serializer_class = RubricaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['descripcion','idcurso']
    search_fields = ['descripcion']
    
class CriterioViewSet(SoftDeleteViewSet):
    queryset = Criterio.objects.order_by('pk')
    serializer_class = CriterioSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['titulo','descripcion',"peso",'idrubrica'  ]
    search_fields = ['titulo','descripcion',"peso"]

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
        
        ids_usuarios = request.data.get('idusers', [])
        idcurso = request.data.get('idcurso')

        if not ids_usuarios or not idcurso:
            return Response({'error': 'Faltan parámetros: idusers o idcurso'}, status=status.HTTP_400_BAD_REQUEST)

        curso = Curso.objects.filter(pk=idcurso).first()
        if not curso:
            return Response({'error': 'Curso no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        errores, creados, reactivados = [], [], []

        for iduser in ids_usuarios:
            try:
                # Paso 1: Matricular en UserCurso
                usercurso = UserCurso.all_objects.filter(iduser_id=iduser, idcurso=curso, rol=7).first()
                if usercurso:
                    if usercurso.eliminado:
                        usercurso.eliminado = 0
                        usercurso.save()
                        reactivados.append(iduser)
                else:
                    UserCurso.objects.create(iduser_id=iduser, idcurso=curso, rol=7)
                    creados.append(iduser)

                # Paso 2: Buscar relaciones UsuarioDesafio (rol=7)
                relaciones_ud = UsuarioDesafio.objects.filter(iduser_id=iduser, rol=7, eliminado=0)

                for ud in relaciones_ud:
                    desafio = ud.idproyecto

                    # Paso 3: Verificar y crear CursoDesafio si no existe
                    curso_desafio = CursoDesafio.objects.filter(idcurso=curso, idproyecto=desafio).first()
                    if not curso_desafio:
                        curso_desafio = CursoDesafio.objects.create(idcurso=curso, idproyecto=desafio)

                    # Paso 4: Asegurar existencia de UsuarioDesafio (activo)
                    ud_existente = UsuarioDesafio.all_objects.filter(
                        iduser_id=iduser, idproyecto=desafio, rol=7
                    ).first()

                    if ud_existente:
                        if ud_existente.eliminado:
                            ud_existente.eliminado = 0
                            ud_existente.save()
                    else:
                        UsuarioDesafio.objects.create(iduser_id=iduser, idproyecto=desafio, rol=7)

            except Exception as e:
                errores.append({'iduser': iduser, 'error': str(e)})

        return Response({
            'mensaje': 'Proceso completado',
            'creados': creados,
            'reactivados': reactivados,
            'errores': errores
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="desmatricular_estudiantes")
    def desmatricular_estudiantes(self, request):
        ids_usuarios = request.data.get('idusers', [])
        idcurso = request.data.get('idcurso')

        if not ids_usuarios or not idcurso:
            return Response({'error': 'Faltan parámetros: idusers o idcurso'}, status=status.HTTP_400_BAD_REQUEST)

        curso = Curso.objects.filter(pk=idcurso).first()
        if not curso:
            return Response({'error': 'Curso no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        desmatriculados, desvinculados_cd, errores = [], [], []

        for iduser in ids_usuarios:
            try:
                # 1. Desactivar la relación UserCurso
                usercurso = UserCurso.objects.filter(iduser_id=iduser, idcurso=curso, rol=7, eliminado=0).first()
                if usercurso:
                    usercurso.eliminado = 1
                    usercurso.save()
                    desmatriculados.append(iduser)

                # 2. Buscar todos los desafíos del usuario (activos, rol=7)
                usuario_desafios = UsuarioDesafio.objects.filter(iduser_id=iduser, rol=7, eliminado=0)

                for ud in usuario_desafios:
                    desafio = ud.idproyecto

                    # Verificar si hay otros usuarios estudiantes activos en este Curso y Desafío
                    curso_desafio = CursoDesafio.objects.filter(idcurso=curso, idproyecto=desafio).first()
                    if curso_desafio:
                        otros_estudiantes = UserCurso.objects.filter(
                            idcurso=curso,
                            rol=7,
                            eliminado=0,
                            iduser_id__in=UsuarioDesafio.objects.filter(
                                idproyecto=desafio,
                                rol=7,
                                eliminado=0
                            ).exclude(iduser_id=iduser).values_list('iduser_id', flat=True)
                        )

                        # Si ya no hay más estudiantes activos, eliminar la relación CursoDesafio
                        if not otros_estudiantes.exists():
                            curso_desafio.delete()
                            desvinculados_cd.append({'curso': idcurso, 'desafio': desafio.pk})

            except Exception as e:
                errores.append({'iduser': iduser, 'error': str(e)})

        return Response({
            'mensaje': 'Desmatriculación completada',
            'desmatriculados': desmatriculados,
            'curso_desafio_desvinculados': desvinculados_cd,
            'errores': errores
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
from django_filters import rest_framework as dfilters

# Define un filtro personalizado
class CursoDesafioFilter(FilterSet):
    idcursos = dfilters.BaseInFilter(field_name='idcurso', lookup_expr='in')
    jurado = dfilters.NumberFilter(method='filter_by_jurado')
    
    class Meta:
        model = CursoDesafio
        fields = ['idproyecto', 'idcurso', 'idplanformacion', 'idcurso__titulo']
    def filter_by_jurado(self, queryset, name, value):
        return queryset.filter(
            Q(idjurado1=value) | Q(idjurado2=value) | Q(idjurado3=value)
        )


class CursoDesafioViewSet(SoftDeleteViewSet):
    queryset = CursoDesafio.objects.select_related(
        'idcurso', 'idproyecto'
    ).order_by('pk')
    serializer_class = CursoDesafioSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_class = CursoDesafioFilter  # Usar la clase de filtro personalizada
    search_fields = ['idproyecto__titulo', 'idcurso__titulo', 'idcurso']
    
    
    
    
class UsuarioDesafioViewSet(SoftDeleteViewSet):
    queryset = UsuarioDesafio.objects.order_by('pk')
    serializer_class = UsuarioDesafioSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_fields = ['iduser', 'idproyecto', 'iduser_id__nombres', 'idproyecto__titulo','rol']
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
    search_fields = ['idrol__titulo', 'iduser__nombres', 'iduser__apellidos', 'iduser__email']
    
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
    

from django.db import connection
from rest_framework.views import APIView

class DetallesCompletosFuncion2View(APIView):
    def get(self, request):
        anio = request.GET.get('anio')  # filtro opcional de ejemplo

        query = "SELECT * FROM traer_detalles_completos_18()"
        if anio:
            query = f"""
                SELECT * FROM traer_detalles_completos_18()
                WHERE anioacademico_curso = {int(anio)}
            """

        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            results = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]

        return JsonResponse(results, safe=False)

    
    
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







from rest_framework import viewsets, filters
from rest_framework.response import Response
from django.db import connection
from .serializers import DetallesCompletosSerializer
from .models import DetallesCompletos
from .filters import DateTimeIntervalFilter

# Custom filter backend for raw procedure data
class CustomFilterBackend:
    def filter_queryset(self, request, queryset, view):
        # Get filter parameters from the request
        filterset_fields = getattr(view, 'filterset_fields', [])
        filtered_queryset = queryset
        
        # Apply filters manually
        for field in filterset_fields:
            value = request.query_params.get(field, None)
            if value is not None:
                filtered_queryset = [
                    item for item in filtered_queryset
                    if getattr(item, field, None) == value or 
                       (isinstance(getattr(item, field, None), str) and 
                        value.lower() in getattr(item, field, '').lower())
                ]
        
        return filtered_queryset

# Custom search backend for raw procedure data
class CustomSearchBackend:
    def filter_queryset(self, request, queryset, view):
        search_term = request.query_params.get('search', None)
        if not search_term:
            return queryset
            
        search_fields = getattr(view, 'search_fields', [])
        if not search_fields:
            return queryset
            
        # Simple search implementation
        results = []
        for item in queryset:
            for field in search_fields:
                field_value = getattr(item, field, '')
                if field_value and search_term.lower() in str(field_value).lower():
                    results.append(item)
                    break
                    
        return results

# Custom ordering backend
class CustomOrderingBackend:
    def filter_queryset(self, request, queryset, view):
        ordering = request.query_params.get('ordering', None)
        if ordering is None:
            return queryset
            
        ordering_fields = getattr(view, 'ordering_fields', [])
        if not ordering or not ordering_fields:
            return queryset
            
        reverse = False
        if ordering.startswith('-'):
            reverse = True
            ordering = ordering[1:]
            
        if ordering in ordering_fields:
            return sorted(
                queryset, 
                key=lambda obj: getattr(obj, ordering, ''),
                reverse=reverse
            )
            
        return queryset

class ProcedimientoModelViewSet(viewsets.ModelViewSet):
    """
    ViewSet base personalizado para trabajar con procedimientos almacenados
    """
    def get_queryset(self):
        return DetallesCompletos.objects.none()
    
    def list(self, request, *args, **kwargs):
        # Obtenemos los datos directamente del procedimiento
        resultados = DetallesCompletos.detalles.get_from_procedure()
        
        # Mostrar en la consola para depuración
        print(f"Resultados obtenidos: {len(resultados)}")
        if resultados:
            print(f"Ejemplo de item: {resultados[0]}")
        
        # Aplicar filtros - VERSIÓN CORREGIDA
        filtered_results = resultados
        
        # Debugging - mostrar parámetros recibidos
        print(f"Query params: {request.query_params}")
        
        # Filtrar por cada parámetro excepto los especiales
        for param, value in request.query_params.items():
            if param not in ['search', 'ordering', 'page', 'page_size', 'format']:
                # Antes del filtrado
                count_before = len(filtered_results)
                print(f"Filtrando por {param}={value}, resultados antes: {count_before}")
                
                # Implementación más flexible del filtrado
                temp_results = []
                for item in filtered_results:
                    # Convertir a string para comparación (si existe el campo)
                    if param in item:
                        item_value = str(item.get(param, '')).lower()
                        param_value = str(value).lower()
                        
                        # Compara de forma flexible
                        if param_value in item_value or param_value == item_value:
                            temp_results.append(item)
                
                filtered_results = temp_results
                
                # Después del filtrado
                print(f"Resultados después: {len(filtered_results)}")
        
        # Aplicar búsqueda
        search_term = request.query_params.get('search')
        if search_term and hasattr(self, 'search_fields'):
            count_before = len(filtered_results)
            print(f"Aplicando búsqueda por '{search_term}', resultados antes: {count_before}")
            
            search_results = []
            for item in filtered_results:
                found = False
                for field in self.search_fields:
                    if field in item:
                        field_value = str(item.get(field, '')).lower()
                        if search_term.lower() in field_value:
                            search_results.append(item)
                            found = True
                            break
            
            filtered_results = search_results
            print(f"Resultados después de búsqueda: {len(filtered_results)}")
        
        # Aplicar ordenamiento
        ordering = request.query_params.get('ordering')
        if ordering and hasattr(self, 'ordering_fields'):
            reverse = False
            if ordering.startswith('-'):
                reverse = True
                ordering = ordering[1:]
            
            if ordering in self.ordering_fields:
                try:
                    filtered_results = sorted(
                        filtered_results,
                        key=lambda x: str(x.get(ordering, '')).lower(),
                        reverse=reverse
                    )
                    print(f"Ordenado por {ordering} {'descendente' if reverse else 'ascendente'}")
                except Exception as e:
                    print(f"Error al ordenar: {e}")
        
        # Paginamos
        page = self.paginate_queryset(filtered_results)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(filtered_results, many=True)
        return Response(serializer.data)

class DetallesCompletosViewSet(ProcedimientoModelViewSet):
    serializer_class = DetallesCompletosSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['titulo_curso', 'nombre_usuario', 'titulo_desafio']
    ordering_fields = ['titulo_curso', 'nombre_usuario', 'nivel_curso', 'titulo_desafio']
    filterset_class = DetallesCompletosFilter