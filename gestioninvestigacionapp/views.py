from rest_framework.viewsets import ModelViewSet
from gestioninvestigacionapp.serializers import ActividadSerializer, ArchivoSerializer, ArchivoActividadesSerializer, ArchivoPostulacionesSerializer, ComponenteSerializer, ConvocatoriaSerializer, CursoSerializer, DepartamentoSerializer, DesafioSerializer, EntregableSerializer, EvaluacionSerializer, NotificcionesSerializer, PlantesisSerializer, PostulanteSerializer, PresupuestoSerializer, ReporteSerializer, RetroalimentacionSerializer, RetroalimentacionacttecnicaSerializer, RubricaSerializer, UserSerializer, ActividadcronogramaSerializer, ActividadtecnicaSerializer, PostulacionSerializer, PostulacionPropuestaSerializer, UserCursoSerializer, UsuarioDesafioSerializer
from gestioninvestigacionapp.models import Actividad, Archivo, ArchivoActividades, ArchivoPostulaciones, Componente, Convocatoria, Curso, Departamento, Desafio, Entregable, Evaluacion, Notificciones, Plantesis, Postulante, Presupuesto, Reporte, Retroalimentacion, Retroalimentacionacttecnica, Rubrica, User, Actividadcronograma, Actividadtecnica, Postulacion, PostulacionPropuesta, UserCurso, UsuarioDesafio


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
    queryset = User.objects.order_by('pk')
    serializer_class = UserSerializer


class ActividadcronogramaViewSet(ModelViewSet):
    queryset = Actividadcronograma.objects.order_by('pk')
    serializer_class = ActividadcronogramaSerializer


class ActividadtecnicaViewSet(ModelViewSet):
    queryset = Actividadtecnica.objects.order_by('pk')
    serializer_class = ActividadtecnicaSerializer


class PostulacionViewSet(ModelViewSet):
    queryset = Postulacion.objects.order_by('pk')
    serializer_class = PostulacionSerializer


class PostulacionPropuestaViewSet(ModelViewSet):
    queryset = PostulacionPropuesta.objects.order_by('pk')
    serializer_class = PostulacionPropuestaSerializer


class UserCursoViewSet(ModelViewSet):
    queryset = UserCurso.objects.order_by('pk')
    serializer_class = UserCursoSerializer


class UsuarioDesafioViewSet(ModelViewSet):
    queryset = UsuarioDesafio.objects.order_by('pk')
    serializer_class = UsuarioDesafioSerializer
