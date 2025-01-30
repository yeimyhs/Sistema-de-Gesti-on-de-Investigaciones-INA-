from rest_framework.serializers import ModelSerializer
from gestioninvestigacionapp.models import Actividad, Archivo, ArchivoActividades, ArchivoPostulaciones, Componente, Convocatoria, Curso, Departamento, Desafio, Entregable, Evaluacion, Notificciones, Plantesis, Postulante, Presupuesto, Reporte, Retroalimentacion, Retroalimentacionacttecnica, Rubrica, User, Actividadcronograma, Actividadtecnica, Postulacion, PostulacionPropuesta, UserCurso, UsuarioDesafio


class ActividadSerializer(ModelSerializer):

    class Meta:
        model = Actividad
        fields = '__all__'


class ArchivoSerializer(ModelSerializer):

    class Meta:
        model = Archivo
        fields = '__all__'


class ArchivoActividadesSerializer(ModelSerializer):

    class Meta:
        model = ArchivoActividades
        fields = '__all__'


class ArchivoPostulacionesSerializer(ModelSerializer):

    class Meta:
        model = ArchivoPostulaciones
        fields = '__all__'


class ComponenteSerializer(ModelSerializer):

    class Meta:
        model = Componente
        fields = '__all__'


class ConvocatoriaSerializer(ModelSerializer):

    class Meta:
        model = Convocatoria
        fields = '__all__'


class CursoSerializer(ModelSerializer):

    class Meta:
        model = Curso
        fields = '__all__'


class DepartamentoSerializer(ModelSerializer):

    class Meta:
        model = Departamento
        fields = '__all__'


class DesafioSerializer(ModelSerializer):

    class Meta:
        model = Desafio
        fields = '__all__'


class EntregableSerializer(ModelSerializer):

    class Meta:
        model = Entregable
        fields = '__all__'


class EvaluacionSerializer(ModelSerializer):

    class Meta:
        model = Evaluacion
        fields = '__all__'


class NotificcionesSerializer(ModelSerializer):

    class Meta:
        model = Notificciones
        fields = '__all__'


class PlantesisSerializer(ModelSerializer):

    class Meta:
        model = Plantesis
        fields = '__all__'


class PostulanteSerializer(ModelSerializer):

    class Meta:
        model = Postulante
        fields = '__all__'


class PresupuestoSerializer(ModelSerializer):

    class Meta:
        model = Presupuesto
        fields = '__all__'


class ReporteSerializer(ModelSerializer):

    class Meta:
        model = Reporte
        fields = '__all__'


class RetroalimentacionSerializer(ModelSerializer):

    class Meta:
        model = Retroalimentacion
        fields = '__all__'


class RetroalimentacionacttecnicaSerializer(ModelSerializer):

    class Meta:
        model = Retroalimentacionacttecnica
        fields = '__all__'


class RubricaSerializer(ModelSerializer):

    class Meta:
        model = Rubrica
        fields = '__all__'


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class ActividadcronogramaSerializer(ModelSerializer):

    class Meta:
        model = Actividadcronograma
        fields = '__all__'


class ActividadtecnicaSerializer(ModelSerializer):

    class Meta:
        model = Actividadtecnica
        fields = '__all__'


class PostulacionSerializer(ModelSerializer):

    class Meta:
        model = Postulacion
        fields = '__all__'


class PostulacionPropuestaSerializer(ModelSerializer):

    class Meta:
        model = PostulacionPropuesta
        fields = '__all__'


class UserCursoSerializer(ModelSerializer):

    class Meta:
        model = UserCurso
        fields = '__all__'


class UsuarioDesafioSerializer(ModelSerializer):

    class Meta:
        model = UsuarioDesafio
        fields = '__all__'
