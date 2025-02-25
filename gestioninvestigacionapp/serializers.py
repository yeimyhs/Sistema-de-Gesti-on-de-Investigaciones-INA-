from rest_framework.serializers import ModelSerializer
from gestioninvestigacionapp.models import Actividad, Archivo, ArchivoActividades, ArchivoPostulaciones, Componente, Convocatoria, Curso, Departamento, Desafio, Entregable, Evaluacion, Notificciones, Plantesis, Postulante, Presupuesto, Reporte, Retroalimentacion, Retroalimentacionacttecnica, Rubrica, Actividadcronograma, Actividadtecnica, PostulacionPropuesta, UserCurso, UsuarioDesafio
from .models import *

from .models import CustomUser
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

User = get_user_model()

class UserCursoSerializer(ModelSerializer):
    curso_titulo = serializers.CharField(source="idcurso.titulo", read_only=True)
    
    class Meta:
        model = UserCurso
        fields = '__all__'


class CustomUserSerializer(ModelSerializer):
    cursos = UserCursoSerializer(source="usercurso_set", many=True, read_only=True)
    class Meta:
        #depth = 1
        model = CustomUser
        fields = ['activo',
            'id',
            "nombres",
            "apellidos",
            "fechacreacion",
            "telefono",
            "fotoperfil",
            "activo",
            "instituto",
            "pais",
            "ciudad",
            "email",
            
            'email_verified_at',
            'remember_token',
            'is_staff',
            'cursos'
        ]
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.hashers import make_password
from .models import CustomUser  # Asegúrate de importar tu modelo de usuario

class RegisterSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'password',
            "nombres",
            "apellidos",
            "fechacreacion",
            "telefono",
            "fotoperfil",
            "activo",
            "instituto",
            "pais",
            "ciudad",
            "email",
            "gradoacademico",
            "zipcode",
            
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """ Sobrescribe la creación del usuario para encriptar la contraseña """
        validated_data['password'] = make_password(validated_data['password'])  # Encripta la contraseña
        return super().create(validated_data)

class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(label="Email del usuario")
    password = serializers.CharField(label="Contraseña", style={"input_type": "password"})

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        # Validar si faltan campos
        if not email and not password:
            raise serializers.ValidationError(
                {
                    "error": {
                        "code": "missing_fields",
                        "message": "El nombre de usuario y la contraseña son obligatorios."
                    }
                },
                code="authorization",
            )
        elif not email:
            raise serializers.ValidationError(
                {
                    "error": {
                        "code": "missing_username",
                        "message": "El nombre de usuario es obligatorio."
                    }
                },
                code="authorization",
            )
        elif not password:
            raise serializers.ValidationError(
                {
                    "error": {
                        "code": "missing_password",
                        "message": "La contraseña es obligatoria."
                    }
                },
                code="authorization",
            )

        # Autenticar al usuario
        #user = authenticate(email=email, password=password)
        user = User.objects.filter(email=email).first()

        if user and user.check_password(password):
            # Validar credenciales inválidas
            if not user:
                raise serializers.ValidationError(
                    {
                        "error": {
                            "code": "invalid_credentials",
                            "message": "Las credenciales proporcionadas no son válidas. Por favor, intente de nuevo."
                        }
                    },
                    code="authorization",
                )

            # Verificar si la cuenta está deshabilitada
            if not user.activo:
                raise serializers.ValidationError(
                    {
                        "error": {
                            "code": "account_disabled",
                            "message": "Esta cuenta está deshabilitada. Contacte con el administrador."
                        }
                    },
                    code="authorization",
                )

            # Validar si el usuario está inactivo
            if not user.is_active:
                raise serializers.ValidationError(
                    {
                        "error": {
                            "code": "account_inactive",
                            "message": "Esta cuenta está inactiva. Por favor, contacte con el administrador."
                        }
                    },
                    code="authorization",
                )

        # Si todo es válido, se retorna el usuario
        attrs["user"] = user
        return attrs
    
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
    departamento = serializers.SerializerMethodField()
    class Meta:
        model = Convocatoria
        fields = '__all__'
    
    
    def get_departamento(self, obj):
        """
        Obtiene los departamentos asociados a la convocatoria a través de los desafíos y cursos.
        """
        try:
            desafios = obj.desafio_set.all()  # Obtener todos los desafíos de la convocatoria
            departamentos = set()  # Usamos un conjunto para evitar duplicados

            for desafio in desafios:
                if desafio.idcurso and desafio.idcurso.iddepartamento:
                    departamentos.add((desafio.idcurso.iddepartamento.iddepartamento, desafio.idcurso.iddepartamento.nombre))

            return [{"id": dep[0], "nombre": dep[1]} for dep in departamentos] if departamentos else None
        except AttributeError:
            return None 

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




class ActividadcronogramaSerializer(ModelSerializer):

    class Meta:
        model = Actividadcronograma
        fields = '__all__'


class ActividadtecnicaSerializer(ModelSerializer):

    class Meta:
        model = Actividadtecnica
        fields = '__all__'



class PostulacionPropuestaSerializer(ModelSerializer):

    class Meta:
        model = PostulacionPropuesta
        fields = '__all__'


class UserCursoSerializer(ModelSerializer):
    curso_titulo = serializers.CharField(source="idcurso.titulo", read_only=True)
    
    class Meta:
        model = UserCurso
        fields = '__all__'


class UsuarioDesafioSerializer(ModelSerializer):

    class Meta:
        model = UsuarioDesafio
        fields = '__all__'


class EstadoSerializer(ModelSerializer):

    class Meta:
        model = Estado
        fields = '__all__'


class ubigeoDepartamentoSerializer(ModelSerializer):

    class Meta:
        model = ubigeoDepartamento
        fields = '__all__'



class ubigeoProvinciaSerializer(ModelSerializer):

    class Meta:
        model = ubigeoProvincia
        fields = '__all__'



class ubigeoDistritoSerializer(ModelSerializer):

    class Meta:
        model = Estado
        fields = '__all__'


