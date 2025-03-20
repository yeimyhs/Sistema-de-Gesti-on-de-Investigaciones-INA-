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



class Rol(models.Model):
    
    identificador_rol = models.BigAutoField(primary_key=True) 
    #nombre_tabla = models.CharField(max_length=255, help_text="Nombre de la tabla a la que pertenece este estado")
    #identificador_tabla = models.CharField(max_length=255, help_text="Identificador único del registro dentro de la tabla")  # ID de la tabla relacionada
    descripcion = models.TextField(blank=True, null=True)  # Descripción opcional
    titulo = models.CharField(max_length=255)  # Título del rol

    def __str__(self):
        return f"{self.titulo}"


class Estado(models.Model):
    nombre_tabla = models.CharField(max_length=255, help_text="Nombre de la tabla a la que pertenece este estado")
    identificador_tabla = models.CharField(max_length=255, help_text="Identificador único del registro dentro de la tabla")
    descripcion = models.CharField(max_length=255)
    clave = models.CharField(max_length=255, help_text="Clave del estado")
    valor = models.CharField(help_text="Valor del estado")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('nombre_tabla', 'identificador_tabla', 'clave')
        indexes = [
            models.Index(fields=['nombre_tabla', 'identificador_tabla']),
        ]

    def __str__(self):
        return f"{self.nombre_tabla} ({self.identificador_tabla}): {self.clave} = {self.valor}"

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
    
    GRADO_ACADEMICO_CHOICES = [
        ('Secundaria', 'Secundaria'),
        ('Bachillerato', 'Bachillerato'),
        ('Universitario', 'Universitario'),
        ('Maestría', 'Maestría'),
        ('Doctorado', 'Doctorado'),
        ('Otro', 'Otro'),
    ]
    # Eliminar el campo `username` heredado
    username = None
    
    # Campos adicionales
    nombres = models.CharField(max_length=128)
    fechacreacion = models.DateTimeField(auto_now_add=True)
    apellidos = models.CharField(max_length=128, blank=True, null=True)
    telefono = models.CharField(max_length=255, blank=True, null=True)
    fotoperfil = models.ImageField(upload_to='perfilUsuarioimagen/', blank=True, null=True)
    eliminado = models.BooleanField(default =1)
    
    instituto = models.CharField(max_length=128, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    pais = models.CharField(max_length=128, blank=True, null=True)
    ciudad = models.CharField(max_length=128, blank=True, null=True)
    
    
    gradoacademico = models.CharField(
        max_length=20,
        choices=GRADO_ACADEMICO_CHOICES,
        blank=True,
        null=True,
        default='Otro'
    )
    zipcode = models.CharField(max_length=20, blank=True, null=True)
    
    email = models.EmailField(unique=True) 
    email_verified_at = models.DateTimeField(blank=True, null=True)
    remember_token = models.CharField(max_length=100, blank=True, null=True)


    plataforma = models.SmallIntegerField()
    estado = models.SmallIntegerField()

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



class ubigeoPais(models.Model):
    idpais = models.CharField(max_length=255,primary_key=True)
    nombre = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'ubigeoPais'


class ubigeoDepartamento(models.Model):
    iddepartamento = models.CharField(max_length=255,primary_key=True)
    nombre = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'ubigeoDepartamento'


class ubigeoProvincia(models.Model):
    idprovincia = models.CharField(max_length=255,primary_key=True)
    nombre = models.CharField(max_length=255)
    iddepartamento = models.ForeignKey(ubigeoDepartamento, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'ubigeoProvincia'


class ubigeoDistrito(models.Model):
    idciudad = models.CharField(max_length=255,primary_key=True)
    nombre = models.CharField(max_length=255)
    idprovincia = models.ForeignKey(ubigeoProvincia, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'ubigeoDistrito'


#-------------------------------------------------------------------------------------------------------------user
class Actividad(models.Model):
    fechacreacion = models.DateTimeField(auto_now_add=True)
    idactividad = models.BigAutoField(primary_key=True)
    idproyecto = models.ForeignKey('Desafio', models.DO_NOTHING, db_column='idproyecto')
    tipo = models.BigIntegerField(blank=True, null=True)
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    fechaentrega = models.DateField()
    eliminado = models.BooleanField(default=0)
    estado = models.SmallIntegerField()

    class Meta:
        db_table = 'Actividad'


class Archivo(models.Model):
    fechacreacion = models.DateTimeField(auto_now_add=True)
    nombre = models.CharField(max_length=255)
    ubicacion = models.FileField(upload_to='archivosConvocatoriaDesafio/', blank=True, null=True)

    eliminado = models.BooleanField(default=0)
    idarchivo = models.BigAutoField(primary_key=True)
    idconvocatoria = models.ForeignKey('Convocatoria', models.DO_NOTHING, db_column='idconvocatoria', blank=True, null=True)
    idproyecto = models.ForeignKey('Desafio', models.DO_NOTHING, db_column='idproyecto', blank=True, null=True)

    class Meta:
        db_table = 'Archivo'


class ArchivoActividades(models.Model):
    fechacreacion = models.DateTimeField(auto_now_add=True)
    nombre = models.CharField(max_length=255)
    ubicacion = models.FileField(upload_to='archivosActividad/', blank=True, null=True)

    eliminado = models.BooleanField(default=0)
    idarchivo = models.BigAutoField(primary_key=True)
    idactividad = models.ForeignKey(Actividad, models.DO_NOTHING, db_column='idactividad', blank=True, null=True)

    class Meta:
        db_table = 'Archivo_actividades'


class ArchivoPostulaciones(models.Model):
    fechacreacion = models.DateTimeField(auto_now_add=True)
    nombre = models.CharField(max_length=255)
    ubicacion = models.FileField(upload_to='archivosPostulacion/', blank=True, null=True)
   
    eliminado = models.BooleanField(default=0)
    idarchivo = models.BigAutoField(primary_key=True)
    idconvocatoria = models.BigIntegerField(blank=True, null=True)
    idproyecto = models.ForeignKey('PostulacionPropuesta', models.DO_NOTHING, db_column='idproyecto', blank=True, null=True)

    class Meta:
        db_table = 'Archivo_postulaciones'


class DatosTecnicos(models.Model):
    descripcion = models.TextField( blank=True, null=True)
    fechacreacion = models.DateTimeField(auto_now_add=True)
    iddatostecnicos = models.BigAutoField(primary_key=True)

    class Meta:
        db_table = 'DatosTecnicos'


class Componente(models.Model):
    fechacreacion = models.DateTimeField(auto_now_add=True)
    idcomponente = models.BigAutoField(primary_key=True)
    numero = models.BigIntegerField()
    iddatostecnicos = models.ForeignKey(DatosTecnicos, models.DO_NOTHING, db_column='idproyecto', blank=True, null=True)

    class Meta:
        db_table = 'Componente'


class Convocatoria(models.Model):
    GRADO_CHOICES = [
        ('Pregrado', 'Pregrado'),
        ('Posgrado', 'Posgrado'),
    ]
    
    idconvocatoria = models.BigAutoField(primary_key=True)
    fechacreacion = models.DateTimeField(auto_now_add=True)
    fechainicio = models.DateTimeField(blank=True, null=True)
    fechafin = models.DateTimeField(blank=True, null=True)
    fechaevaluacion = models.DateTimeField(blank=True, null=True)
    grado = models.CharField(max_length=20,
        choices=GRADO_CHOICES,
        blank=True,
        null=True,
        default='Otro'
    )
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    eliminado = models.BooleanField(default=0)
    estado = models.SmallIntegerField()
    objetivogeneral = models.TextField(blank=True, null=True)
    prioridadesconvocatoria = models.TextField(blank=True, null=True)
    publicoobjetivo = models.TextField(blank=True, null=True)
    imagen = models.ImageField(upload_to='convocatoriaimagen/', blank=True, null=True)

    class Meta:
        db_table = 'Convocatoria'


class Curso(models.Model):
    fechacreacion = models.DateTimeField(auto_now_add=True)
    idcurso = models.BigAutoField(primary_key=True)
    titulo = models.CharField(max_length=255)
    nivel = models.CharField(max_length=255, blank=True, null=True)
    anioacademico = models.IntegerField()
    semestre = models.SmallIntegerField(blank=True, null=True)
    #coordinador = models.CharField(max_length=255, blank=True, null=True)
    fecharegistro = models.DateField()
    estado = models.SmallIntegerField()
    eliminado = models.BooleanField(default=0)
    iddepartamento = models.ForeignKey('Departamento', models.DO_NOTHING, db_column='iddepartamento', blank=True, null=True)
    idrubrica = models.ForeignKey('Rubrica', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'Curso'


class Departamento(models.Model):
    fechacreacion = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to='departamentoimagen/', blank=True, null=True)
    iddepartamento = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    lugar = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255)
    telefono = models.CharField(max_length=255, blank=True, null=True)
    director = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, db_column='iduser')
    
    estado = models.SmallIntegerField()
    eliminado = models.BooleanField(default=0)
    
    class Meta:
        db_table = 'Departamento'


class Desafio(models.Model):
    fechacreacion = models.DateTimeField(auto_now_add=True)
    idproyecto = models.BigAutoField(primary_key=True)
    idconvocatoria = models.ForeignKey(Convocatoria, models.DO_NOTHING, db_column='idconvocatoria', blank=True, null=True)
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    estado = models.SmallIntegerField()
    eliminado = models.BooleanField(default=0)
    personalequiposcriticos = models.TextField(blank=True, null=True)
    razon = models.TextField(blank=True, null=True)
    requerimientominimos = models.TextField(blank=True, null=True)
    imagen = models.ImageField(upload_to='desafioimagen/', blank=True, null=True)
 
    areasinvestigacion = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'Desafio'

class Entregable(models.Model):
    fechacreacion = models.DateTimeField(auto_now_add=True)
    identregable = models.BigAutoField(primary_key=True)
    pdfentregable = models.TextField()
    comentario = models.TextField(blank=True, null=True)
    idactividadtecnica = models.ForeignKey('Actividadtecnica', models.DO_NOTHING, db_column='idactividadTecnica', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Entregable'


class Evaluacion(models.Model):
    fechacreacion = models.DateTimeField(auto_now_add=True)
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
    fechacreacion = models.DateTimeField(auto_now_add=True)
    idnotificacion = models.BigAutoField(primary_key=True)
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    eliminado = models.BooleanField(default=0)
    iduser = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, db_column='iduser', blank=True, null=True)

    class Meta:
        db_table = 'Notificciones'


class Plantesis(models.Model):
    fechacreacion = models.DateTimeField(auto_now_add=True)
    idplanformacion = models.BigAutoField(primary_key=True)
    titulo = models.CharField(max_length=255, blank=True, null=True)
    justificacion = models.CharField(max_length=255, blank=True, null=True)
    abstract = models.CharField(max_length=255)
    objgeneral = models.TextField(blank=True, null=True)
    objetivosespecificos = models.TextField(blank=True, null=True)  # This field type is a guess.
    #verificar si los campos seran json
    class Meta:
        db_table = 'PlanTesis'


class Postulante(models.Model):
    fechacreacion = models.DateTimeField(auto_now_add=True)
    iduser = models.BigAutoField(primary_key=True)
    nombres = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    institucion = models.CharField(max_length=255, blank=True, null=True)
    eliminado = models.BooleanField(default=0)
    pais = models.CharField(max_length=255, blank=True, null=True)
    ciudad = models.CharField(max_length=255, blank=True, null=True)
    fotoperfil = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=255, blank=True, null=True)
    idproyecto = models.ForeignKey('PostulacionPropuesta', models.DO_NOTHING, db_column='idproyecto', blank=True, null=True)

    class Meta:
        db_table = 'Postulante'


class Presupuesto(models.Model):
    fechacreacion = models.DateTimeField(auto_now_add=True)
    idproyecto = models.ForeignKey(Desafio, models.DO_NOTHING, db_column='idproyecto', blank=True, null=True)
    partida = models.CharField(max_length=255)
    monto = models.FloatField()
    idpresupuesto = models.BigAutoField(primary_key=True)

    class Meta:
        db_table = 'Presupuesto'


class Reporte(models.Model):
    fechacreacion = models.DateTimeField(auto_now_add=True)
    idreporte = models.BigAutoField(primary_key=True)
    evaluacionnota = models.BigIntegerField(blank=True, null=True)
    pdf = models.BigIntegerField(blank=True, null=True)
    idactividad = models.ForeignKey(Actividad, models.DO_NOTHING, db_column='idactividad', blank=True, null=True)

    class Meta:
        db_table = 'Reporte'


class Retroalimentacion(models.Model):
    fechacreacion = models.DateTimeField(auto_now_add=True)
    idretroalimentacion = models.BigAutoField(primary_key=True)
    idreporte = models.ForeignKey(Reporte, models.DO_NOTHING, db_column='idreporte', blank=True, null=True)
    comentario = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'Retroalimentacion'


class Retroalimentacionacttecnica(models.Model):
    fechacreacion = models.DateTimeField(auto_now_add=True)
    idretroalimentacion = models.BigAutoField(primary_key=True)
    identregable = models.ForeignKey(Entregable, models.DO_NOTHING, db_column='identregable', blank=True, null=True)
    comentario = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'Retroalimentacionacttecnica'


class Rubrica(models.Model):
    descripcion = models.TextField( blank=True, null=True)
    fechacreacion = models.DateTimeField(auto_now_add=True)
    idrubrica = models.BigAutoField(primary_key=True)

    class Meta:
        db_table = 'Rubrica'

class Criterio(models.Model):
    fechacreacion = models.DateTimeField(auto_now_add=True)
    idcriterio = models.BigAutoField(primary_key=True)
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField( blank=True, null=True)
    peso = models.FloatField()
    puntaje = models.FloatField()
    idrubrica = models.ForeignKey(Rubrica, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'Criterio'



class Actividadcronograma(models.Model):
    fechacreacion = models.DateTimeField(auto_now_add=True)
    titulo = models.CharField(max_length=255)
    eliminado = models.BooleanField(default=0)
    fechainicial = models.DateField(blank=True, null=True)
    fechafinal = models.DateField(blank=True, null=True)
    idactividad = models.BigAutoField(primary_key=True)
    idconvocatoria = models.ForeignKey('Convocatoria', models.DO_NOTHING, db_column='idconvocatoria', blank=True, null=True)

    class Meta:
        db_table = 'actividadCronograma'


class Actividadtecnica(models.Model):
    fechacreacion = models.DateTimeField(auto_now_add=True)
    idactividadtecnica = models.BigIntegerField(db_column='idactividadTecnica', primary_key=True)  # Field name made lowercase.
    tipo = models.BigIntegerField(blank=True, null=True)
    idcomponente = models.ForeignKey(Componente, models.DO_NOTHING, db_column='idcomponente')
    estado = models.IntegerField()
    fechainicio = models.DateField(blank=True, null=True)
    fechafinal = models.DateField(blank=True, null=True)
    eliminado = models.DateField()
    titulo = models.CharField(max_length=255)

    class Meta:
        db_table = 'actividadTecnica'





class PostulacionPropuesta(models.Model):
    id =  models.BigAutoField(primary_key=True)
    
    fechacreacion = models.DateTimeField(auto_now_add=True)
    idproyecto = models.ForeignKey(Desafio, models.DO_NOTHING, db_column='idproyecto')
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
    estado = models.SmallIntegerField()

    class Meta:
        db_table = 'postulacion_propuesta'


class UserCurso(models.Model):
    id =  models.BigAutoField(primary_key=True)
    
    fechacreacion = models.DateTimeField(auto_now_add=True)
    iduser = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, db_column='iduser')
    idcurso = models.ForeignKey(Curso, models.DO_NOTHING, db_column='idcurso')
    rol = models.SmallIntegerField()

    class Meta:
        db_table = 'user_curso'
        #borar porque  un profe pude ser tbn un coordinador
        #unique_together = (
        #    ('iduser', 'idcurso'),)


class CursoDesafio(models.Model):
    id =  models.BigAutoField(primary_key=True)
    idproyecto = models.ForeignKey(Desafio, models.DO_NOTHING, db_column='idproyecto')
    iddatostecnicos = models.ForeignKey(DatosTecnicos, models.DO_NOTHING, blank=True, null=True)
    fechacreacion = models.DateTimeField(auto_now_add=True)
    idcurso = models.ForeignKey(Curso, models.DO_NOTHING, db_column='idcurso')
    idplanformacion = models.ForeignKey(Plantesis, models.DO_NOTHING, blank=True, null=True)
    

    class Meta:
        db_table = 'curso_desafio'
        unique_together = (('idproyecto', 'idcurso'),)


class UsuarioDesafio(models.Model):
    id =  models.BigAutoField(primary_key=True)
    
    fechacreacion = models.DateTimeField(auto_now_add=True)
    iduser = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, db_column='iduser')
    idproyecto = models.ForeignKey(Desafio, models.DO_NOTHING, db_column='idproyecto')
    rol = models.SmallIntegerField()

    class Meta:
        db_table = 'usuario_desafio'
        unique_together = (('iduser', 'idproyecto'),)


class UsuarioRolSistema(models.Model):
    id =  models.BigAutoField(primary_key=True)
    
    fechacreacion = models.DateTimeField(auto_now_add=True)
    iduser = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, db_column='iduser')
    idrol = models.ForeignKey(Rol, models.DO_NOTHING, db_column='idrol')

    class Meta:
        db_table = 'usuario_rol'
        unique_together = (('iduser', 'idrol'),)




