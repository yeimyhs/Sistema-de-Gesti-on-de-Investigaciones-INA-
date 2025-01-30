from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from gestioninvestigacionapp.serializers import ActividadSerializer, ArchivoSerializer, ArchivoActividadesSerializer, ArchivoPostulacionesSerializer, ComponenteSerializer, ConvocatoriaSerializer, CursoSerializer, DepartamentoSerializer, DesafioSerializer, EntregableSerializer, EvaluacionSerializer, NotificcionesSerializer, PlantesisSerializer, PostulanteSerializer, PresupuestoSerializer, ReporteSerializer, RetroalimentacionSerializer, RetroalimentacionacttecnicaSerializer, RubricaSerializer, UserSerializer, ActividadcronogramaSerializer, ActividadtecnicaSerializer, PostulacionSerializer, PostulacionPropuestaSerializer, UserCursoSerializer, UsuarioDesafioSerializer
from gestioninvestigacionapp.models import Actividad, Archivo, ArchivoActividades, ArchivoPostulaciones, Componente, Convocatoria, Curso, Departamento, Desafio, Entregable, Evaluacion, Notificciones, Plantesis, Postulante, Presupuesto, Reporte, Retroalimentacion, Retroalimentacionacttecnica, Rubrica, User, Actividadcronograma, Actividadtecnica, Postulacion, PostulacionPropuesta, UserCurso, UsuarioDesafio


class ActividadViewSet(ViewSet):

    def list(self, request):
        queryset = Actividad.objects.order_by('pk')
        serializer = ActividadSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ActividadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = Actividad.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = ActividadSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = Actividad.objects.get(pk=pk)
        except Actividad.DoesNotExist:
            return Response(status=404)
        serializer = ActividadSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = Actividad.objects.get(pk=pk)
        except Actividad.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class ArchivoViewSet(ViewSet):

    def list(self, request):
        queryset = Archivo.objects.order_by('pk')
        serializer = ArchivoSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ArchivoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = Archivo.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = ArchivoSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = Archivo.objects.get(pk=pk)
        except Archivo.DoesNotExist:
            return Response(status=404)
        serializer = ArchivoSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = Archivo.objects.get(pk=pk)
        except Archivo.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class ArchivoActividadesViewSet(ViewSet):

    def list(self, request):
        queryset = ArchivoActividades.objects.order_by('pk')
        serializer = ArchivoActividadesSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ArchivoActividadesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = ArchivoActividades.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = ArchivoActividadesSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = ArchivoActividades.objects.get(pk=pk)
        except ArchivoActividades.DoesNotExist:
            return Response(status=404)
        serializer = ArchivoActividadesSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = ArchivoActividades.objects.get(pk=pk)
        except ArchivoActividades.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class ArchivoPostulacionesViewSet(ViewSet):

    def list(self, request):
        queryset = ArchivoPostulaciones.objects.order_by('pk')
        serializer = ArchivoPostulacionesSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ArchivoPostulacionesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = ArchivoPostulaciones.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = ArchivoPostulacionesSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = ArchivoPostulaciones.objects.get(pk=pk)
        except ArchivoPostulaciones.DoesNotExist:
            return Response(status=404)
        serializer = ArchivoPostulacionesSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = ArchivoPostulaciones.objects.get(pk=pk)
        except ArchivoPostulaciones.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class ComponenteViewSet(ViewSet):

    def list(self, request):
        queryset = Componente.objects.order_by('pk')
        serializer = ComponenteSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ComponenteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = Componente.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = ComponenteSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = Componente.objects.get(pk=pk)
        except Componente.DoesNotExist:
            return Response(status=404)
        serializer = ComponenteSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = Componente.objects.get(pk=pk)
        except Componente.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class ConvocatoriaViewSet(ViewSet):

    def list(self, request):
        queryset = Convocatoria.objects.order_by('pk')
        serializer = ConvocatoriaSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ConvocatoriaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = Convocatoria.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = ConvocatoriaSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = Convocatoria.objects.get(pk=pk)
        except Convocatoria.DoesNotExist:
            return Response(status=404)
        serializer = ConvocatoriaSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = Convocatoria.objects.get(pk=pk)
        except Convocatoria.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class CursoViewSet(ViewSet):

    def list(self, request):
        queryset = Curso.objects.order_by('pk')
        serializer = CursoSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CursoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = Curso.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = CursoSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = Curso.objects.get(pk=pk)
        except Curso.DoesNotExist:
            return Response(status=404)
        serializer = CursoSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = Curso.objects.get(pk=pk)
        except Curso.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class DepartamentoViewSet(ViewSet):

    def list(self, request):
        queryset = Departamento.objects.order_by('pk')
        serializer = DepartamentoSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = DepartamentoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = Departamento.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = DepartamentoSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = Departamento.objects.get(pk=pk)
        except Departamento.DoesNotExist:
            return Response(status=404)
        serializer = DepartamentoSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = Departamento.objects.get(pk=pk)
        except Departamento.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class DesafioViewSet(ViewSet):

    def list(self, request):
        queryset = Desafio.objects.order_by('pk')
        serializer = DesafioSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = DesafioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = Desafio.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = DesafioSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = Desafio.objects.get(pk=pk)
        except Desafio.DoesNotExist:
            return Response(status=404)
        serializer = DesafioSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = Desafio.objects.get(pk=pk)
        except Desafio.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class EntregableViewSet(ViewSet):

    def list(self, request):
        queryset = Entregable.objects.order_by('pk')
        serializer = EntregableSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = EntregableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = Entregable.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = EntregableSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = Entregable.objects.get(pk=pk)
        except Entregable.DoesNotExist:
            return Response(status=404)
        serializer = EntregableSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = Entregable.objects.get(pk=pk)
        except Entregable.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class EvaluacionViewSet(ViewSet):

    def list(self, request):
        queryset = Evaluacion.objects.order_by('pk')
        serializer = EvaluacionSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = EvaluacionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = Evaluacion.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = EvaluacionSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = Evaluacion.objects.get(pk=pk)
        except Evaluacion.DoesNotExist:
            return Response(status=404)
        serializer = EvaluacionSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = Evaluacion.objects.get(pk=pk)
        except Evaluacion.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class NotificcionesViewSet(ViewSet):

    def list(self, request):
        queryset = Notificciones.objects.order_by('pk')
        serializer = NotificcionesSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = NotificcionesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = Notificciones.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = NotificcionesSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = Notificciones.objects.get(pk=pk)
        except Notificciones.DoesNotExist:
            return Response(status=404)
        serializer = NotificcionesSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = Notificciones.objects.get(pk=pk)
        except Notificciones.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class PlantesisViewSet(ViewSet):

    def list(self, request):
        queryset = Plantesis.objects.order_by('pk')
        serializer = PlantesisSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = PlantesisSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = Plantesis.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = PlantesisSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = Plantesis.objects.get(pk=pk)
        except Plantesis.DoesNotExist:
            return Response(status=404)
        serializer = PlantesisSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = Plantesis.objects.get(pk=pk)
        except Plantesis.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class PostulanteViewSet(ViewSet):

    def list(self, request):
        queryset = Postulante.objects.order_by('pk')
        serializer = PostulanteSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = PostulanteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = Postulante.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = PostulanteSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = Postulante.objects.get(pk=pk)
        except Postulante.DoesNotExist:
            return Response(status=404)
        serializer = PostulanteSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = Postulante.objects.get(pk=pk)
        except Postulante.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class PresupuestoViewSet(ViewSet):

    def list(self, request):
        queryset = Presupuesto.objects.order_by('pk')
        serializer = PresupuestoSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = PresupuestoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = Presupuesto.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = PresupuestoSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = Presupuesto.objects.get(pk=pk)
        except Presupuesto.DoesNotExist:
            return Response(status=404)
        serializer = PresupuestoSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = Presupuesto.objects.get(pk=pk)
        except Presupuesto.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class ReporteViewSet(ViewSet):

    def list(self, request):
        queryset = Reporte.objects.order_by('pk')
        serializer = ReporteSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ReporteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = Reporte.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = ReporteSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = Reporte.objects.get(pk=pk)
        except Reporte.DoesNotExist:
            return Response(status=404)
        serializer = ReporteSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = Reporte.objects.get(pk=pk)
        except Reporte.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class RetroalimentacionViewSet(ViewSet):

    def list(self, request):
        queryset = Retroalimentacion.objects.order_by('pk')
        serializer = RetroalimentacionSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = RetroalimentacionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = Retroalimentacion.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = RetroalimentacionSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = Retroalimentacion.objects.get(pk=pk)
        except Retroalimentacion.DoesNotExist:
            return Response(status=404)
        serializer = RetroalimentacionSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = Retroalimentacion.objects.get(pk=pk)
        except Retroalimentacion.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class RetroalimentacionacttecnicaViewSet(ViewSet):

    def list(self, request):
        queryset = Retroalimentacionacttecnica.objects.order_by('pk')
        serializer = RetroalimentacionacttecnicaSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = RetroalimentacionacttecnicaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = Retroalimentacionacttecnica.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = RetroalimentacionacttecnicaSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = Retroalimentacionacttecnica.objects.get(pk=pk)
        except Retroalimentacionacttecnica.DoesNotExist:
            return Response(status=404)
        serializer = RetroalimentacionacttecnicaSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = Retroalimentacionacttecnica.objects.get(pk=pk)
        except Retroalimentacionacttecnica.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class RubricaViewSet(ViewSet):

    def list(self, request):
        queryset = Rubrica.objects.order_by('pk')
        serializer = RubricaSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = RubricaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = Rubrica.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = RubricaSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = Rubrica.objects.get(pk=pk)
        except Rubrica.DoesNotExist:
            return Response(status=404)
        serializer = RubricaSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = Rubrica.objects.get(pk=pk)
        except Rubrica.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class UserViewSet(ViewSet):

    def list(self, request):
        queryset = User.objects.order_by('pk')
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=404)
        serializer = UserSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class ActividadcronogramaViewSet(ViewSet):

    def list(self, request):
        queryset = Actividadcronograma.objects.order_by('pk')
        serializer = ActividadcronogramaSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ActividadcronogramaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = Actividadcronograma.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = ActividadcronogramaSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = Actividadcronograma.objects.get(pk=pk)
        except Actividadcronograma.DoesNotExist:
            return Response(status=404)
        serializer = ActividadcronogramaSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = Actividadcronograma.objects.get(pk=pk)
        except Actividadcronograma.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class ActividadtecnicaViewSet(ViewSet):

    def list(self, request):
        queryset = Actividadtecnica.objects.order_by('pk')
        serializer = ActividadtecnicaSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ActividadtecnicaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = Actividadtecnica.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = ActividadtecnicaSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = Actividadtecnica.objects.get(pk=pk)
        except Actividadtecnica.DoesNotExist:
            return Response(status=404)
        serializer = ActividadtecnicaSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = Actividadtecnica.objects.get(pk=pk)
        except Actividadtecnica.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class PostulacionViewSet(ViewSet):

    def list(self, request):
        queryset = Postulacion.objects.order_by('pk')
        serializer = PostulacionSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = PostulacionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = Postulacion.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = PostulacionSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = Postulacion.objects.get(pk=pk)
        except Postulacion.DoesNotExist:
            return Response(status=404)
        serializer = PostulacionSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = Postulacion.objects.get(pk=pk)
        except Postulacion.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class PostulacionPropuestaViewSet(ViewSet):

    def list(self, request):
        queryset = PostulacionPropuesta.objects.order_by('pk')
        serializer = PostulacionPropuestaSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = PostulacionPropuestaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = PostulacionPropuesta.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = PostulacionPropuestaSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = PostulacionPropuesta.objects.get(pk=pk)
        except PostulacionPropuesta.DoesNotExist:
            return Response(status=404)
        serializer = PostulacionPropuestaSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = PostulacionPropuesta.objects.get(pk=pk)
        except PostulacionPropuesta.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class UserCursoViewSet(ViewSet):

    def list(self, request):
        queryset = UserCurso.objects.order_by('pk')
        serializer = UserCursoSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = UserCursoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = UserCurso.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = UserCursoSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = UserCurso.objects.get(pk=pk)
        except UserCurso.DoesNotExist:
            return Response(status=404)
        serializer = UserCursoSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = UserCurso.objects.get(pk=pk)
        except UserCurso.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class UsuarioDesafioViewSet(ViewSet):

    def list(self, request):
        queryset = UsuarioDesafio.objects.order_by('pk')
        serializer = UsuarioDesafioSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = UsuarioDesafioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = UsuarioDesafio.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = UsuarioDesafioSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = UsuarioDesafio.objects.get(pk=pk)
        except UsuarioDesafio.DoesNotExist:
            return Response(status=404)
        serializer = UsuarioDesafioSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = UsuarioDesafio.objects.get(pk=pk)
        except UsuarioDesafio.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)
