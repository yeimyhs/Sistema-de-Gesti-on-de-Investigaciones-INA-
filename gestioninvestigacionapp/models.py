# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remov` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Actividad(models.Model):
    idactividad = models.BigIntegerField(primary_key=True)
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
    idarchivo = models.BigIntegerField(primary_key=True)
    idconvocatoria = models.ForeignKey('Convocatoria', models.DO_NOTHING, db_column='idconvocatoria', blank=True, null=True)
    idproyecto = models.ForeignKey('Desafio', models.DO_NOTHING, db_column='idproyecto', blank=True, null=True)

    class Meta:
        db_table = 'Archivo'


class ArchivoActividades(models.Model):
    nombre = models.CharField(max_length=20)
    ubicacion = models.TextField()
    activo = models.BooleanField()
    fechacreacion = models.DateField()
    idarchivo = models.BigIntegerField(primary_key=True)
    idactividad = models.ForeignKey(Actividad, models.DO_NOTHING, db_column='idactividad', blank=True, null=True)

    class Meta:
        db_table = 'Archivo_actividades'


class ArchivoPostulaciones(models.Model):
    nombre = models.CharField(max_length=20)
    ubicacion = models.TextField()
    activo = models.BooleanField()
    fechacreacion = models.DateField()
    idarchivo = models.BigIntegerField(primary_key=True)
    idconvocatoria = models.BigIntegerField(blank=True, null=True)
    idproyecto = models.ForeignKey('PostulacionPropuesta', models.DO_NOTHING, db_column='idproyecto', blank=True, null=True)

    class Meta:
        db_table = 'Archivo_postulaciones'


class Componente(models.Model):
    idcomponente = models.BigIntegerField(primary_key=True)
    numero = models.BigIntegerField()
    idproyecto = models.ForeignKey('Desafio', models.DO_NOTHING, db_column='idproyecto', blank=True, null=True)

    class Meta:
        db_table = 'Componente'


class Convocatoria(models.Model):
    idconvocatoria = models.BigIntegerField(primary_key=True)
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
    idcurso = models.BigIntegerField(primary_key=True)
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
    iddepartamento = models.BigIntegerField(primary_key=True)
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
    idproyecto = models.BigIntegerField(primary_key=True)
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
    identregable = models.BigIntegerField(primary_key=True)
    pdfentregable = models.TextField()
    comentario = models.TextField(blank=True, null=True)
    idactividadtecnica = models.ForeignKey('Actividadtecnica', models.DO_NOTHING, db_column='idactividadTecnica', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Entregable'


class Evaluacion(models.Model):
    idevaluacion = models.BigIntegerField(primary_key=True)
    comentario = models.TextField()
    pionero = models.FloatField()
    rentable = models.FloatField()
    practico = models.FloatField()
    total = models.FloatField()
    idplanformacion = models.ForeignKey('Plantesis', models.DO_NOTHING, db_column='idplanformacion', blank=True, null=True)

    class Meta:
        db_table = 'Evaluacion'


class Notificciones(models.Model):
    idnotificacion = models.BigIntegerField(primary_key=True)
    titulo = models.CharField(max_length=20)
    descripcion = models.TextField()
    activo = models.BooleanField()
    fechacreacion = models.DateField()
    iduser = models.ForeignKey('User', models.DO_NOTHING, db_column='iduser', blank=True, null=True)

    class Meta:
        db_table = 'Notificciones'


class Plantesis(models.Model):
    idplanformacion = models.BigIntegerField(primary_key=True)
    idproyecto = models.ForeignKey(Desafio, models.DO_NOTHING, db_column='idproyecto', blank=True, null=True)
    titulo = models.CharField(max_length=20, blank=True, null=True)
    justificacion = models.CharField(max_length=20, blank=True, null=True)
    abstract = models.CharField(max_length=20)
    objgeneral = models.TextField(blank=True, null=True)
    objetivosespecificos = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        db_table = 'PlanTesis'


class Postulante(models.Model):
    iduser = models.BigIntegerField(primary_key=True)
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
    idpresupuesto = models.BigIntegerField(primary_key=True)

    class Meta:
        db_table = 'Presupuesto'


class Reporte(models.Model):
    idreporte = models.BigIntegerField(primary_key=True)
    evaluacionnota = models.BigIntegerField(blank=True, null=True)
    pdf = models.BigIntegerField(blank=True, null=True)
    idactividad = models.ForeignKey(Actividad, models.DO_NOTHING, db_column='idactividad', blank=True, null=True)

    class Meta:
        db_table = 'Reporte'


class Retroalimentacion(models.Model):
    idretroalimentacion = models.BigIntegerField(primary_key=True)
    idreporte = models.ForeignKey(Reporte, models.DO_NOTHING, db_column='idreporte', blank=True, null=True)
    comentario = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'Retroalimentacion'


class Retroalimentacionacttecnica(models.Model):
    idretroalimentacion = models.BigIntegerField(primary_key=True)
    identregable = models.ForeignKey(Entregable, models.DO_NOTHING, db_column='identregable', blank=True, null=True)
    comentario = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'Retroalimentacionacttecnica'


class Rubrica(models.Model):
    idproyecto = models.ForeignKey(Desafio, models.DO_NOTHING, db_column='idproyecto', blank=True, null=True)
    idrubrica = models.BigIntegerField(primary_key=True)

    class Meta:
        db_table = 'Rubrica'


class User(models.Model):
    iduser = models.BigIntegerField(primary_key=True)
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

    class Meta:
        db_table = 'User'


class Actividadcronograma(models.Model):
    titulo = models.CharField(max_length=20)
    fechacreacion = models.DateField()
    activo = models.BooleanField()
    fechainicial = models.DateField(blank=True, null=True)
    fechafinal = models.DateField(blank=True, null=True)
    idactividad = models.BigIntegerField(primary_key=True)

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


class Postulacion(models.Model):
    idconvocatoria = models.OneToOneField(Convocatoria, models.DO_NOTHING, db_column='idconvocatoria', primary_key=True)

    class Meta:
        db_table = 'postulacion'


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
    iduser = models.OneToOneField(User, models.DO_NOTHING, db_column='iduser', primary_key=True)
    idcurso = models.ForeignKey(Curso, models.DO_NOTHING, db_column='idcurso')
    rol = models.SmallIntegerField()

    class Meta:
        db_table = 'user_curso'
        unique_together = (('iduser', 'idcurso'),)


class UsuarioDesafio(models.Model):
    iduser = models.OneToOneField(User, models.DO_NOTHING, db_column='iduser', primary_key=True)
    idproyecto = models.ForeignKey(Desafio, models.DO_NOTHING, db_column='idproyecto')
    rol = models.SmallIntegerField()

    class Meta:
        db_table = 'usuario_desafio'
        unique_together = (('iduser', 'idproyecto'),)
