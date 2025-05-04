from rest_framework.serializers import ModelSerializer
from gestioninvestigacionapp.models import Actividad, Archivo, ArchivoActividades, Componente, Convocatoria, Curso, Departamento, Desafio, Entregable, Evaluacion, Notificciones, Plantesis, Postulante, Presupuesto, Reporte, Retroalimentacion, Retroalimentacionacttecnica, Rubrica, Actividadcronograma, Actividadtecnica, PostulacionPropuesta, UserCurso, UsuarioDesafio
from .models import *

from .models import CustomUser
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

User = get_user_model()
class UserSimpleDetalleSerializer(ModelSerializer):
    class Meta:
        #depth = 1
        model = CustomUser
        fields = ['eliminado',
            'id',
            "nombres",
            "apellidos",
            "fechacreacion",
            "telefono",
            "dni",
            "fotoperfil",
            "instituto",
            "pais",
            "ciudad",
            "email",
            "direccion",
            
            "gradoacademico",
            "zipcode",
            
            'email_verified_at',
            'remember_token',
            
            "estado"
        ]
class UsuarioSimpleSerializer(ModelSerializer):
    class Meta:
        #depth = 1
        model = CustomUser
        fields = [
            'id',
            "nombres",
            "apellidos",
            "telefono",
            
            "instituto",
            "email",
            "direccion",
            
            "gradoacademico",
            
        ]
class OnlyDepartamentonombreSerializer(ModelSerializer):

    class Meta:
        model = Departamento
        fields = ['nombre']
        
class OnlyCursoSerializer(ModelSerializer):
    departamentodetalle = OnlyDepartamentonombreSerializer(source='iddepartamento', many=False, required=False)

    class Meta:
        model = Curso
        fields = '__all__'
        
        

class UserCursoSerializer(ModelSerializer):
    curso_titulo = serializers.CharField(source="idcurso.titulo", read_only=True)
    
    class Meta:
        model = UserCurso
        fields = '__all__'


class UserCursoFulldetalleSerializer(ModelSerializer):
    iduser = UserSimpleDetalleSerializer(read_only=True)  # Incluye los detalles del usuario
    idcurso = OnlyCursoSerializer(read_only=True)
    
    class Meta:
        model = UserCurso
        fields = '__all__'




class CustomUserSerializer(ModelSerializer):
    cursos = UserCursoSerializer(source="usercurso_set", many=True, read_only=True)
    roles = serializers.SerializerMethodField()
    class Meta:
        #depth = 1
        model = CustomUser
        fields = ['eliminado',
            'id',
            "nombres",
            "apellidos",
            "fechacreacion",
            "dni",
            "telefono",
            "fotoperfil",
            "instituto",
            "pais",
            "ciudad",
            "email",
            "direccion",
            
            "gradoacademico",
            "zipcode",
            
            'email_verified_at',
            'remember_token',
            'cursos',
            
            "estado",
            'roles'
            
        ]
    def get_roles(self, obj):
        # Obtener los roles del usuario en una sola consulta
        roles = Rol.objects.filter(usuariorolsistema__iduser=obj).values('identificador_rol', 'titulo')
        return list(roles)
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
            "dni",
            "telefono",
            "fotoperfil",
            "eliminado",
            "instituto",
            "direccion",
            "pais",
            "ciudad",
            "email",
            "gradoacademico",
            "zipcode",
            
            "estado",
            
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """ Sobrescribe la creación del usuario para encriptar la contraseña """
        validated_data['password'] = make_password(validated_data['password'])  # Encripta la contraseña
        return super().create(validated_data)

class UserCursoDetalleUserSerializer(ModelSerializer):
    #curso_titulo = serializers.CharField(source="idcurso.titulo", read_only=True)
    userdetalle = UserSimpleDetalleSerializer(source='iduser', many=False, required=False, read_only=True)
    
    class Meta:
        model = UserCurso
        fields = '__all__'

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
       
        user = authenticate(request=self.context.get('request'), username=email, password=password)

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
            if user.eliminado:
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
    
class ArchivoActividadesSerializer(ModelSerializer):

    class Meta:
        model = ArchivoActividades
        fields = '__all__'

    
class ActividadSerializer(ModelSerializer):
    fechaentrega = serializers.DateTimeField(format="%d/%m/%Y %H:%M")
    creador = UserSimpleDetalleSerializer(source='iduser',read_only=True)
    archivos = ArchivoActividadesSerializer(source='archivoactividades_set', many=True, read_only=True)
    class Meta:
        model = Actividad
        fields = '__all__'
    def create(self, validated_data):
        request = self.context['request']
        archivos_data = self.context['request'].FILES.getlist('archivos')  # Obtiene los archivos enviados
        actividad = Actividad.objects.create(**validated_data)  # Crea la convocatoria en la BD

        archivosnombres_data = request.data.get('archivosnombres', '[]')
        archivosnombres_data = json.loads(request.data.get('archivosnombres', '[]'))  # Asegurar que sea una lista

        for archivo, archivonombre in zip( archivos_data,archivosnombres_data):
        
            extension = os.path.splitext(archivo.name)[1]  # Extrae la extensión original (ej: .pdf, .jpg)
            nuevo_nombre = f"{actividad.titulo}{extension}"  # Usa el título como nombre del archivo

            
            # Crear instancia de Archivo con el archivo renombrado
            archivo_instance = ArchivoActividades(
                nombre=archivonombre,
                ubicacion=archivo,  # Guarda el archivo real
                fechacreacion=now(),
                idactividad=actividad
            )

            # Renombrar el archivo antes de guardarlo
            archivo_instance.ubicacion.save(nuevo_nombre, ContentFile(archivo.read()), save=True)

        return actividad
    def update(self, instance, validated_data):
        request = self.context['request']
        
        # Obtener archivos enviados y sus nombres
        archivos_data = request.FILES.getlist('archivos')
        archivosnombres_data = json.loads(request.data.get('archivosnombres', '[]'))  # Asegurar que sea una lista

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # ✅ Guardar cambios en la instancia antes de manejar archivos
        instance.save()

        instance.archivo_set.all().delete()

        # 📂 Agregar nuevos archivos con nombres personalizados
        for archivo, archivonombre in zip(archivos_data, archivosnombres_data):
            extension = os.path.splitext(archivo.name)[1]  # Extraer la extensión original
            nuevo_nombre = f"{instance.titulo}{extension}"  # Nombre basado en el título del Desafio

            archivo_instance = ArchivoActividades(
                nombre=archivonombre,
                fechacreacion=now(),
                idactividad=instance
            )
            
            # 📌 Guardar el archivo en la ubicación correcta
            archivo_instance.ubicacion.save(nuevo_nombre, ContentFile(archivo.read()), save=True)

        return instance



class ConfiguracionSerializer(ModelSerializer):

    class Meta:
        model = Configuracion
        fields = '__all__'



class ArchivoSerializer(ModelSerializer):

    class Meta:
        model = Archivo
        fields = '__all__'





class ComponenteSerializer(ModelSerializer):

    class Meta:
        model = Componente
        fields = '__all__'


class DatosTecnicosSerializer(ModelSerializer):

    class Meta:
        model = DatosTecnicos
        fields = '__all__'


class ActividadcronogramaSerializer(ModelSerializer):

    class Meta:
        model = Actividadcronograma
        fields = '__all__'


class DepartamentoSerializer(ModelSerializer):
    directordetalle = UserSimpleDetalleSerializer(source='director',read_only=True)

    class Meta:
        model = Departamento
        fields = '__all__'

class ConvocatoriaOnlyDepSerializer(ModelSerializer):
    departamentodetalle = DepartamentoSerializer(source='iddepartamento', many=False, required=False)
    class Meta:
        model = Convocatoria
        fields = '__all__'

class OnlyDesafioSerializer(ModelSerializer):

    class Meta:
        model = Desafio
        fields = '__all__'
        
        
class DesafioSerializer(ModelSerializer):
    archivos = ArchivoSerializer(source='archivo_set', many=True, read_only=True)
    idconvocatoriadetalle = ConvocatoriaOnlyDepSerializer(source='idconvocatoria', many=False, required=False, read_only=True)
    jurados = serializers.SerializerMethodField()
    asesores = serializers.SerializerMethodField()
    class Meta:
        model = Desafio
        fields = '__all__'
    
    def get_jurados(self, obj):
        usuarios = UsuarioDesafio.objects.filter(idproyecto=obj, rol=10, eliminado=0).select_related('iduser')
        return UsuarioSimpleSerializer([u.iduser for u in usuarios], many=True).data

    def get_asesores(self, obj):
        usuarios = UsuarioDesafio.objects.filter(idproyecto=obj, rol=9, eliminado=0).select_related('iduser')
        return UsuarioSimpleSerializer([u.iduser for u in usuarios], many=True).data
        
    def create(self, validated_data):
        request = self.context['request']
        archivos_data = self.context['request'].FILES.getlist('archivos')  # Obtiene los archivos enviados
        desafio = Desafio.objects.create(**validated_data)  # Crea la convocatoria en la BD

        archivosnombres_data = request.data.get('archivosnombres', '[]')
        archivosnombres_data = json.loads(request.data.get('archivosnombres', '[]'))  # Asegurar que sea una lista

        for archivo, archivonombre in zip( archivos_data,archivosnombres_data):
        
            extension = os.path.splitext(archivo.name)[1]  # Extrae la extensión original (ej: .pdf, .jpg)
            nuevo_nombre = f"{desafio.titulo}{extension}"  # Usa el título como nombre del archivo

            
            # Crear instancia de Archivo con el archivo renombrado
            archivo_instance = Archivo(
                nombre=archivonombre,
                ubicacion=archivo,  # Guarda el archivo real
                fechacreacion=now(),
                idproyecto=desafio,
                idconvocatoria=None
            )

            # Renombrar el archivo antes de guardarlo
            archivo_instance.ubicacion.save(nuevo_nombre, ContentFile(archivo.read()), save=True)

        return desafio
    def update(self, instance, validated_data):
        request = self.context['request']
        
        # Obtener archivos enviados y sus nombres
        archivos_data = request.FILES.getlist('archivos')
        archivosnombres_data = json.loads(request.data.get('archivosnombres', '[]'))  # Asegurar que sea una lista

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # ✅ Guardar cambios en la instancia antes de manejar archivos
        instance.save()

        instance.archivo_set.all().delete()

        # 📂 Agregar nuevos archivos con nombres personalizados
        for archivo, archivonombre in zip(archivos_data, archivosnombres_data):
            extension = os.path.splitext(archivo.name)[1]  # Extraer la extensión original
            nuevo_nombre = f"{instance.titulo}{extension}"  # Nombre basado en el título del Desafio

            archivo_instance = Archivo(
                nombre=archivonombre,
                fechacreacion=now(),
                idproyecto=instance,
                idconvocatoria=None
            )
            
            # 📌 Guardar el archivo en la ubicación correcta
            archivo_instance.ubicacion.save(nuevo_nombre, ContentFile(archivo.read()), save=True)

        return instance



from django.utils.timezone import now
import os
from django.core.files.base import ContentFile
import json


    
class ConvocatoriaSerializer(ModelSerializer):
    archivos = ArchivoSerializer(source='archivo_set', many=True, required=False)
    actividades = ActividadcronogramaSerializer(source='actividadcronograma_set', many=True, required=False)
    desafios = OnlyDesafioSerializer(source='desafio_set', many=True, required=False)
    departamentodetalle = DepartamentoSerializer(source='iddepartamento', many=False, required=False)

    class Meta:
        model = Convocatoria
        fields = '__all__'

        
    def create(self, validated_data):
        request = self.context['request']
        archivos_data = self.context['request'].FILES.getlist('archivos')  # Obtiene los archivos enviados
        convocatoria = Convocatoria.objects.create(**validated_data)  # Crea la convocatoria en la BD
        imagen_data = request.FILES.get('imagen', None)
        # Obtener actividades desde 'data' y convertir de JSON a lista de diccionarios
        actividades_json = request.data.get('actividades', '[]')  # Si no se envía, usar lista vacía
        actividades_data = json.loads(actividades_json) if actividades_json else []
        
        # Obtener desafíos desde 'data' y convertir de JSON a lista de IDs
        desafios_json = request.data.get('desafios', '[]')
        desafios_ids = json.loads(desafios_json) if desafios_json else []
        
        archivosnombres_data = request.data.get('archivosnombres', '[]')
        archivosnombres_data = json.loads(request.data.get('archivosnombres', '[]'))  # Asegurar que sea una lista

        for archivo, archivonombre in zip( archivos_data,archivosnombres_data):
            extension = os.path.splitext(archivo.name)[1]  # Extrae la extensión original (ej: .pdf, .jpg)
            nuevo_nombre = f"{convocatoria.titulo}{extension}"  # Usa el título como nombre del archivo

            # Crear instancia de Archivo con el archivo renombrado
            archivo_instance = Archivo(
                nombre=archivonombre,
                ubicacion=archivo,  # Guarda el archivo real
                fechacreacion=now(),
                idconvocatoria=convocatoria,
                idproyecto=None
            )

            # Renombrar el archivo antes de guardarlo
            archivo_instance.ubicacion.save(nuevo_nombre, ContentFile(archivo.read()), save=True)

        for actividad_data in actividades_data:
            Actividadcronograma.objects.create(idconvocatoria=convocatoria, **actividad_data)

        # Vincular los desafíos existentes con la convocatoria
        Desafio.objects.filter(idproyecto__in=desafios_ids).update(idconvocatoria=convocatoria)

        if imagen_data:
            convocatoria.imagen.save(imagen_data.name, imagen_data, save=True)
        return convocatoria
    
    def update(self, instance, validated_data):
        request = self.context['request']
        archivos_data = request.FILES.getlist('archivos')  # Obtiene los archivos enviados
        
        # Obtener actividades desde 'data' y convertir de JSON a lista de diccionarios
        actividades_json = request.data.get('actividades', '[]')
        actividades_data = json.loads(actividades_json) if actividades_json else []
        
        # Obtener desafíos desde 'data' y convertir de JSON a lista de IDs
        desafios_json = request.data.get('desafios', '[]')
        nuevos_desafios_ids = set(json.loads(desafios_json) if desafios_json else [])
        imagen_data = request.FILES.get('imagen', None)
        
        # Actualizar la instancia con los nuevos datos
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if imagen_data:
            instance.imagen.save(imagen_data.name, imagen_data, save=True)
        
        
        instance.save()
        archivosnombres_data = json.loads(request.data.get('archivosnombres', '[]'))  # Asegurar que sea una lista
        
        # Eliminar archivos antiguos y agregar los nuevos
        instance.archivo_set.all().delete()
        for archivo, archivonombre in zip( archivos_data,archivosnombres_data):
            extension = os.path.splitext(archivo.name)[1]  # Extrae la extensión original (ej: .pdf, .jpg)
            nuevo_nombre = f"{instance.titulo}"  # Usa el título como nombre del archivo

            archivo_instance = Archivo(
                nombre=archivonombre,
                ubicacion=archivo,  # Guarda el archivo real
                fechacreacion=now(),
                idconvocatoria=instance,
                idproyecto=None
            )
            
            archivo_instance.ubicacion.save(nuevo_nombre, ContentFile(archivo.read()), save=True)
        
        # Eliminar todas las actividades antiguas y agregar las nuevas
        instance.actividadcronograma_set.all().delete()
        for actividad_data in actividades_data:
            Actividadcronograma.objects.create(idconvocatoria=instance, **actividad_data)
        
        #instance.save()
        # Actualizar los desafíos
        desafios_anteriores_ids = set(instance.desafio_set.values_list('idproyecto', flat=True))
        
        # Quitar el idconvocatoria de los desafíos antiguos
        Desafio.objects.filter(idproyecto__in=desafios_anteriores_ids).update(idconvocatoria=None)
        
        # Asignar la convocatoria a los nuevos desafíos
        Desafio.objects.filter(idproyecto__in=nuevos_desafios_ids).update(idconvocatoria=instance)
        
        return instance


class CursoCoordinadorSerializer(serializers.ModelSerializer):
    iduser = UserSimpleDetalleSerializer(read_only=True)  # Incluye los detalles del usuario
  
    class Meta:
        model = UserCurso
        fields = ['iduser']  # Solo necesitamos el usuario, puedes agregar más si lo deseas


class CursoDesafioSerializer(ModelSerializer):
    cursodetalle = OnlyCursoSerializer(source='idcurso', many=False, required=False, read_only=True)
    desafiodetalle = OnlyDesafioSerializer(source='idproyecto', many=False, required=False, read_only=True)

    class Meta:
        model = CursoDesafio
        fields = '__all__'
        


class CursoSerializer(ModelSerializer):
    coordinadores = serializers.SerializerMethodField()
    departamentodetalle = DepartamentoSerializer(source='iddepartamento', many=False, required=False, read_only=True)

    class Meta:
        model = Curso
        fields = '__all__'

    def get_coordinadores(self, obj):
        coordinadores = UserCurso.objects.filter(idcurso=obj, rol=6).select_related('iduser')
        return CursoCoordinadorSerializer(coordinadores, many=True).data




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


class CriterioSerializer(ModelSerializer):

    class Meta:
        model = Criterio
        fields = '__all__'


class RubricaSerializer(ModelSerializer):
    criterios = serializers.SerializerMethodField()

    class Meta:
        model = Rubrica
        fields = '__all__'  # o especifica tus campos, por ejemplo: ['idrubrica', 'nombre', 'criterios']

    def get_criterios(self, obj):
        criterios = Criterio.objects.filter(idrubrica=obj)
        return CriterioSerializer(criterios, many=True).data



class ActividadtecnicaSerializer(ModelSerializer):

    class Meta:
        model = Actividadtecnica
        fields = '__all__'


class PostulacionPropuestaConvocatoriaDetalleSerializer(ModelSerializer):
    desafiodetalle = DesafioSerializer(source='idproyecto', many=False, required=False, read_only=True)
    class Meta:
        model = PostulacionPropuesta
        fields = '__all__'

 

class PostulacionPropuestaSerializer(ModelSerializer):
    userinscripciondetalle = UserSimpleDetalleSerializer(source='iduser', many=False, required=False, read_only=True)
    postulantesdatos = serializers.SerializerMethodField()
    class Meta:
        model = PostulacionPropuesta
        fields = '__all__'

    def get_postulantesdatos(self, obj):
        postulantesdatos = Postulante.objects.filter(idpostulacionpropuesta=obj)
        return PostulanteSerializer(postulantesdatos, many=True, read_only=True).data


class UsuarioDesafioSerializer(ModelSerializer):
    userinscripciondetalle = UserSimpleDetalleSerializer(source='iduser', many=False, required=False, read_only=True)
    desafiodetalle = OnlyDesafioSerializer(source='idproyecto', many=False, required=False, read_only=True)

    class Meta:
        model = UsuarioDesafio
        fields = '__all__'


class EstadoSerializer(ModelSerializer):

    class Meta:
        model = Estado
        fields = '__all__'

class ubigeoPaisSerializer(ModelSerializer):

    class Meta:
        model = ubigeoPais
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

class UsuarioRolSistemaSerializer(ModelSerializer):
    userdetalle = UserSimpleDetalleSerializer(source='iduser', many=False, required=False, read_only=True)

    class Meta:
        model = UsuarioRolSistema
        fields = '__all__'

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'  # Incluir todos los campos del modelo



class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("No se encontró un usuario con ese correo.")
        return value
    
    
class UserCursoCursoDetalleSerializer(ModelSerializer):
    cursodetalle = CursoSerializer(source='idcurso', many=False, required=False, read_only=True)
    
    class Meta:
        model = UserCurso
        fields = '__all__'

class UsuarioDesafioDesafioDetalleSerializer(ModelSerializer):
    desafiodetalle = DesafioSerializer(source='idproyecto', many=False, required=False, read_only=True)

    class Meta:
        model = UsuarioDesafio
        fields = '__all__'

class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'  # Incluir todos los campos del modelo


class HistoriaexitoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historiaexito
        fields = '__all__'  # Incluir todos los campos del modelo



#----------------------------------------
class OnlyCursoBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = '__all__'


class RelacionUsuarioDesafioSerializer(serializers.ModelSerializer):
    desafio = OnlyDesafioSerializer(source='idproyecto')

    class Meta:
        model = UsuarioDesafio
        fields = ['pk', 'rol', 'desafio']

class RelacionUsuarioCursoSerializer(serializers.ModelSerializer):
    curso = OnlyCursoBasicSerializer(source='idcurso')

    class Meta:
        model = UserCurso
        fields = ['pk', 'rol', 'curso']

class DesafiosUsuarioConCursoSerializer(serializers.Serializer):
    usuario = UserSimpleDetalleSerializer()
    relaciones_desafio = RelacionUsuarioDesafioSerializer(many=True)
    relaciones_curso = RelacionUsuarioCursoSerializer(many=True)


class DetallesCompletosSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetallesCompletos
        fields = '__all__'