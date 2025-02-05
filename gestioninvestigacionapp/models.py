# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remov` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

from django.core.exceptions import ValidationError
from django.conf import settings

from django.contrib.auth.models import AbstractUser, BaseUserManager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El email es obligatorio")
        
        email = self.normalize_email(email)
        # Verifica que el campo nombreusuario esté presente
        #if not nombreusuario:
        #    raise ValueError('El campo nombreusuario debe ser declarado')
        
        # Crea el usuario con el nombre de usuario y otros campos extra
        user = self.model( email = email, **extra_fields)
        
        # Establece la contraseña
        if password:
            user.set_password(password)
        
        # Guarda el usuario en la base de datos
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # Establece is_staff y is_superuser para el superusuario
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('nombres', "superuser")

        # Llama a create_user para crear el superusuario
        return self.create_user( email, password, **extra_fields)

class CustomUser(AbstractUser):
    # Eliminar el campo `username` heredado
    username = None
    
    # Campos adicionales
    nombres = models.CharField(max_length=128)
    apellidos = models.CharField(max_length=128, blank=True, null=True)
    fechacreacion = models.DateTimeField(auto_now_add=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    fotoperfil = models.ImageField(upload_to='perfilUsuarioimagen/', blank=True, null=True)
    activo = models.BooleanField(default =1)
    
    instituto = models.CharField(max_length=128, blank=True, null=True)
    pais = models.CharField(max_length=128, blank=True, null=True)
    ciudad = models.CharField(max_length=128, blank=True, null=True)
    
    email = models.EmailField(unique=True) 
    email_verified_at = models.DateTimeField(blank=True, null=True)
    remember_token = models.CharField(max_length=100, blank=True, null=True)

    # Especificar que el campo para autenticar es `nombreusuario`
    USERNAME_FIELD = 'email'
    
    # Campos requeridos adicionales (no necesitas username ya que lo has reemplazado con nombreusuario)
    REQUIRED_FIELDS = ['nombres']  # En Django, `email` es un campo por defecto si lo estás usando como required

    # Manager personalizado
    objects = CustomUserManager()
    
    def __str__(self):
        return self.nombres
    def get_full_name(self):
        return f"{self.nombres} {self.apellidos or ''}".strip()



#-------------------------------------------------------------------------------------------------------------user
class Actividad(models.Model):
    idactividad = models.BigAutoField(primary_key=True)
    idproyecto = models.ForeignKey('Desafio', models.DO_NOTHING, db_column='idproyecto')
    tipo = models.BigIntegerField(blank=True, null=True)
    titulo = models.CharField(max_length=20)
    descripcion = models.TextField()
    fechaentrega = models.DateField()
    fechacreacion = models.DateField()
    activo = models.BooleanField()
    estado = models.SmallIntegerField()

    class Meta:
        db_table = 'Actividad'


class Archivo(models.Model):
    nombre = models.CharField(max_length=20)
    ubicacion = models.TextField()
    activo = models.BooleanField()
    fechacreacion = models.DateField()
    idarchivo = models.BigAutoField(primary_key=True)
    idconvocatoria = models.ForeignKey('Convocatoria', models.DO_NOTHING, db_column='idconvocatoria', blank=True, null=True)
    idproyecto = models.ForeignKey('Desafio', models.DO_NOTHING, db_column='idproyecto', blank=True, null=True)

    class Meta:
        db_table = 'Archivo'


class ArchivoActividades(models.Model):
    nombre = models.CharField(max_length=20)
    ubicacion = models.TextField()
    activo = models.BooleanField()
    fechacreacion = models.DateField()
    idarchivo = models.BigAutoField(primary_key=True)
    idactividad = models.ForeignKey(Actividad, models.DO_NOTHING, db_column='idactividad', blank=True, null=True)

    class Meta:
        db_table = 'Archivo_actividades'


class ArchivoPostulaciones(models.Model):
    nombre = models.CharField(max_length=20)
    ubicacion = models.TextField()
    activo = models.BooleanField()
    fechacreacion = models.DateField()
    idarchivo = models.BigAutoField(primary_key=True)
    idconvocatoria = models.BigIntegerField(blank=True, null=True)
    idproyecto = models.ForeignKey('PostulacionPropuesta', models.DO_NOTHING, db_column='idproyecto', blank=True, null=True)

    class Meta:
        db_table = 'Archivo_postulaciones'


class Componente(models.Model):
    idcomponente = models.BigAutoField(primary_key=True)
    numero = models.BigIntegerField()
    idproyecto = models.ForeignKey('Desafio', models.DO_NOTHING, db_column='idproyecto', blank=True, null=True)

    class Meta:
        db_table = 'Componente'


class Convocatoria(models.Model):
    idconvocatoria = models.BigAutoField(primary_key=True)
    titulo = models.CharField(max_length=20)
    descripcion = models.TextField()
    fechacreacion = models.DateField()
    activo = models.BooleanField()
    estado = models.SmallIntegerField()
    objetivogeneral = models.TextField(blank=True, null=True)
    prioridadesconvocatoria = models.TextField(blank=True, null=True)
    publicoobjetivo = models.TextField(blank=True, null=True)
    imagen = models.BigIntegerField(blank=True, null=True)
    idactividad = models.ForeignKey('Actividadcronograma', models.DO_NOTHING, db_column='idactividad', blank=True, null=True)

    class Meta:
        db_table = 'Convocatoria'


class Curso(models.Model):
    idcurso = models.BigAutoField(primary_key=True)
    titulo = models.CharField(max_length=20)
    nivel = models.CharField(max_length=20, blank=True, null=True)
    anioacademico = models.IntegerField()
    semestre = models.SmallIntegerField(blank=True, null=True)
    coordinador = models.CharField(max_length=20, blank=True, null=True)
    fecharegistro = models.DateField()
    estado = models.SmallIntegerField()
    activo = models.BooleanField()
    iddepartamento = models.ForeignKey('Departamento', models.DO_NOTHING, db_column='iddepartamento', blank=True, null=True)

    class Meta:
        db_table = 'Curso'


class Departamento(models.Model):
    iddepartamento = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=20)
    lugar = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=20)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    director = models.CharField(max_length=20, blank=True, null=True)
    estado = models.SmallIntegerField()
    activo = models.BooleanField()
    fechacreacion = models.DateField()

    class Meta:
        db_table = 'Departamento'


class Desafio(models.Model):
    idproyecto = models.BigAutoField(primary_key=True)
    idconvocatoria = models.ForeignKey(Convocatoria, models.DO_NOTHING, db_column='idconvocatoria', blank=True, null=True)
    idcurso = models.ForeignKey(Curso, models.DO_NOTHING, db_column='idcurso', blank=True, null=True)
    titulo = models.CharField(max_length=20)
    descripcion = models.TextField()
    estado = models.SmallIntegerField()
    activo = models.BooleanField()
    fechacreacion = models.DateField()
    personalequiposcriticos = models.TextField(blank=True, null=True)
    razon = models.TextField(blank=True, null=True)
    requerimientominimos = models.TextField(blank=True, null=True)
    imagen = models.TextField(blank=True, null=True)
    areasinvestigacion = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'Desafio'


class Entregable(models.Model):
    identregable = models.BigAutoField(primary_key=True)
    pdfentregable = models.TextField()
    comentario = models.TextField(blank=True, null=True)
    idactividadtecnica = models.ForeignKey('Actividadtecnica', models.DO_NOTHING, db_column='idactividadTecnica', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Entregable'


class Evaluacion(models.Model):
    idevaluacion = models.BigAutoField(primary_key=True)
    comentario = models.TextField()
    pionero = models.FloatField()
    rentable = models.FloatField()
    practico = models.FloatField()
    total = models.FloatField()
    idplanformacion = models.ForeignKey('Plantesis', models.DO_NOTHING, db_column='idplanformacion', blank=True, null=True)

    class Meta:
        db_table = 'Evaluacion'


class Notificciones(models.Model):
    idnotificacion = models.BigAutoField(primary_key=True)
    titulo = models.CharField(max_length=20)
    descripcion = models.TextField()
    activo = models.BooleanField()
    fechacreacion = models.DateField()
    iduser = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, db_column='iduser', blank=True, null=True)

    class Meta:
        db_table = 'Notificciones'


class Plantesis(models.Model):
    idplanformacion = models.BigAutoField(primary_key=True)
    idproyecto = models.ForeignKey(Desafio, models.DO_NOTHING, db_column='idproyecto', blank=True, null=True)
    titulo = models.CharField(max_length=20, blank=True, null=True)
    justificacion = models.CharField(max_length=20, blank=True, null=True)
    abstract = models.CharField(max_length=20)
    objgeneral = models.TextField(blank=True, null=True)
    objetivosespecificos = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        db_table = 'PlanTesis'


class Postulante(models.Model):
    iduser = models.BigAutoField(primary_key=True)
    nombres = models.CharField(max_length=20)
    apellidos = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    institucion = models.CharField(max_length=20, blank=True, null=True)
    fechacreacion = models.DateField()
    activo = models.BooleanField()
    pais = models.CharField(max_length=20, blank=True, null=True)
    ciudad = models.CharField(max_length=20, blank=True, null=True)
    fotoperfil = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    idproyecto = models.ForeignKey('PostulacionPropuesta', models.DO_NOTHING, db_column='idproyecto', blank=True, null=True)

    class Meta:
        db_table = 'Postulante'


class Presupuesto(models.Model):
    idproyecto = models.ForeignKey(Desafio, models.DO_NOTHING, db_column='idproyecto', blank=True, null=True)
    partida = models.CharField(max_length=20)
    monto = models.FloatField()
    idpresupuesto = models.BigAutoField(primary_key=True)

    class Meta:
        db_table = 'Presupuesto'


class Reporte(models.Model):
    idreporte = models.BigAutoField(primary_key=True)
    evaluacionnota = models.BigIntegerField(blank=True, null=True)
    pdf = models.BigIntegerField(blank=True, null=True)
    idactividad = models.ForeignKey(Actividad, models.DO_NOTHING, db_column='idactividad', blank=True, null=True)

    class Meta:
        db_table = 'Reporte'


class Retroalimentacion(models.Model):
    idretroalimentacion = models.BigAutoField(primary_key=True)
    idreporte = models.ForeignKey(Reporte, models.DO_NOTHING, db_column='idreporte', blank=True, null=True)
    comentario = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'Retroalimentacion'


class Retroalimentacionacttecnica(models.Model):
    idretroalimentacion = models.BigAutoField(primary_key=True)
    identregable = models.ForeignKey(Entregable, models.DO_NOTHING, db_column='identregable', blank=True, null=True)
    comentario = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'Retroalimentacionacttecnica'


class Rubrica(models.Model):
    idproyecto = models.ForeignKey(Desafio, models.DO_NOTHING, db_column='idproyecto', blank=True, null=True)
    idrubrica = models.BigAutoField(primary_key=True)

    class Meta:
        db_table = 'Rubrica'



class Actividadcronograma(models.Model):
    titulo = models.CharField(max_length=20)
    fechacreacion = models.DateField()
    activo = models.BooleanField()
    fechainicial = models.DateField(blank=True, null=True)
    fechafinal = models.DateField(blank=True, null=True)
    idactividad = models.BigAutoField(primary_key=True)

    class Meta:
        db_table = 'actividadCronograma'


class Actividadtecnica(models.Model):
    idactividadtecnica = models.BigIntegerField(db_column='idactividadTecnica', primary_key=True)  # Field name made lowercase.
    tipo = models.BigIntegerField(blank=True, null=True)
    idcomponente = models.ForeignKey(Componente, models.DO_NOTHING, db_column='idcomponente')
    estado = models.IntegerField()
    fechainicio = models.DateField(blank=True, null=True)
    fechafinal = models.DateField(blank=True, null=True)
    activo = models.DateField()
    fechacreacion = models.DateField()
    titulo = models.CharField(max_length=20)

    class Meta:
        db_table = 'actividadTecnica'



class PostulacionPropuesta(models.Model):
    idproyecto = models.OneToOneField(Desafio, models.DO_NOTHING, db_column='idproyecto', primary_key=True)
    detallepropuesta = models.TextField()
    titulo = models.TextField()
    practico = models.FloatField(blank=True, null=True)
    rentable = models.FloatField(blank=True, null=True)
    pionero = models.FloatField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    practicocomentario = models.TextField(blank=True, null=True)
    rentrablecomentario = models.TextField(blank=True, null=True)
    pionerocomentario = models.TextField(blank=True, null=True)
    antecedentes = models.TextField()
    cumplimientorequerimientos = models.TextField()

    class Meta:
        db_table = 'postulacion_propuesta'


class UserCurso(models.Model):
    iduser = models.OneToOneField(settings.AUTH_USER_MODEL, models.DO_NOTHING, db_column='iduser', primary_key=True)
    idcurso = models.ForeignKey(Curso, models.DO_NOTHING, db_column='idcurso')
    rol = models.SmallIntegerField()

    class Meta:
        db_table = 'user_curso'
        unique_together = (('iduser', 'idcurso'),)


class UsuarioDesafio(models.Model):
    iduser = models.OneToOneField(settings.AUTH_USER_MODEL, models.DO_NOTHING, db_column='iduser', primary_key=True)
    idproyecto = models.ForeignKey(Desafio, models.DO_NOTHING, db_column='idproyecto')
    rol = models.SmallIntegerField()

    class Meta:
        db_table = 'usuario_desafio'
        unique_together = (('iduser', 'idproyecto'),)



