from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import render, redirect
from django.contrib import messages
from .utils import import_computers_from_excel
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.db import transaction
from django.template.defaultfilters import slugify
from datetime import datetime
from simple_history.utils import update_change_reason


# Получаем текущее время и дату
now = datetime.now()
class TexnologyApiView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    @staticmethod
    def get(request, *args, **kwargs):
        departament = DepartmentSerializer(Department.objects.all(), many=True).data
        warehouse_manager = WarehouseManagerSerializer(WarehouseManager.objects.all(), many=True).data
        type_compyuter = TypeCompyuterSerializer(TypeCompyuter.objects.all(), many=True).data
        motherboard = MotherboardModelSerializer(Motherboard.objects.all(), many=True).data
        motherboard_model = MotherboardModelSerializer(MotherboardModel.objects.all(), many=True).data
        cpu = CPUSerializer(CPU.objects.all(), many=True).data
        generation = GenerationSerializer(Generation.objects.all(), many=True).data
        frequency = FrequencySerializer(Frequency.objects.all(), many=True).data
        hdd = HDDSerializer(HDD.objects.all(), many=True).data
        ssd = SSDSerializer(SSD.objects.all(), many=True).data
        disk_type = DiskTypeSerializer(DiskType.objects.all(), many=True).data
        ram_type = RAMTypeSerializer(RAMType.objects.all(), many=True).data
        ram_size = RAMSizeSerializer(RAMSize.objects.all(), many=True).data
        gpu = GPUSerializer(GPU.objects.all(), many=True).data
        printer = PrinterSerializer(Printer.objects.all(), many=True).data
        scaner = ScanerSerializer(Scaner.objects.all(), many=True).data
        mfo = MfoSerializer(MFO.objects.all(), many=True).data
        type_webcamera = TypeWebCameraSerializer(TypeWebCamera.objects.all(), many=True).data
        model_webcam = ModelWebCameraSerializer(ModelWebCamera.objects.all(), many=True).data
        type_monitor = MonitorSerializer(Monitor.objects.all(), many=True).data
        program_with_license_and_systemic = ProgramSerializer(Program.objects.filter(license_type='license', type='systemic'), many=True).data
        program_with_license_and_additional = ProgramSerializer(Program.objects.filter(license_type='license', type='additional'), many=True).data
        program_with_no_license_and_systemic = ProgramSerializer(Program.objects.filter(license_type='no-license', type='systemic'), many=True).data
        program_with_no_license_and_additional = ProgramSerializer(Program.objects.filter(license_type='no-license', type='additional'), many=True).data


        data = {
            'departament': departament,
            'warehouse_manager': warehouse_manager,
            'type_compyuter': type_compyuter,
            'motherboard': motherboard,
            'motherboard_model': motherboard_model,
            'cpu': cpu,
            'generation': generation,
            'frequency': frequency,
            'hdd': hdd,
            'ssd': ssd,
            'disk_type': disk_type,
            'ram_type': ram_type,
            'ram_size': ram_size,
            'gpu': gpu,
            'printer': printer,
            'scaner': scaner,
            'mfo': mfo,
            'type_webcamera': type_webcamera,
            'model_webcam': model_webcam,
            'type_monitor': type_monitor,
            'program_with_license_and_systemic': program_with_license_and_systemic,
            'program_with_license_and_additional':program_with_license_and_additional,
            'program_with_no_license_and_systemic':program_with_no_license_and_systemic,
            'program_with_no_license_and_additional':program_with_no_license_and_additional
        }

        return Response(data)


class CoreApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, *args, **kwargs):
        compyuters = Compyuter.objects.all()
        serializer = CompyuterSerializer(compyuters, many=True)
        return Response(serializer.data)


class CompDetailApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, *args, **kwargs):
        slug = kwargs.get('slug')

        if not slug:
            return Response({"error": "Slug not found"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            compyuter = Compyuter.objects.get(slug=slug)
        except:
            return Response({"error": "Slug bo'yicha ma'lumot topilmadi"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CompyuterSerializer(compyuter)
        return Response(serializer.data)


class CompDeleteApiView(APIView):
    @staticmethod
    def delete(request, *args, **kwargs):
        slug = kwargs.get('slug')

        if not slug:
            return Response({"error": "Slug not found"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            Compyuter.objects.get(slug=slug).delete()
        except:
            return Response({"error": "Slug bo'yicha ma'lumot topilmadi"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"message": "Deleted successfully"})


class InfoCompyuterApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, *args, **kwargs):
        all_compyuters = Compyuter.objects.all().count()
        all_worked_compyuters_count = Compyuter.objects.filter(isActive=True).count()
        all_compyuters_with_printer = Compyuter.objects.filter(printer__isnull=False).exclude(printer__name="Нет").distinct().count()
        all_compyuters_with_scaner = Compyuter.objects.filter(scaner__isnull=False).exclude(scaner__name="Нет").distinct().count()
        all_compyuters_with_mfo = Compyuter.objects.filter(mfo=True).distinct().count()
        all_compyuters_with_net = Compyuter.objects.filter(internet=True).distinct().count()
        all_compyuters_with_webcam = Compyuter.objects.filter(type_webcamera__isnull=False).exclude(type_webcamera__name="Нет").distinct().count()
        print(all_compyuters_with_scaner)
        info = {
            "all_compyuters_count": all_compyuters,
            "all_worked_compyuters_count": all_worked_compyuters_count,
            "all_compyuters_with_printer": all_compyuters_with_printer,
            "all_compyuters_with_scaner": all_compyuters_with_scaner,
            "all_compyuters_with_mfo": all_compyuters_with_mfo,
            "all_compyuters_with_webcam": all_compyuters_with_webcam,
            "all_compyuters_with_net": all_compyuters_with_net,
        }
        return Response(info)


class AddCompyuterApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, *args, **kwargs):
        request.data['addedUser'] = request.user.id
        serializer = AddCompyuterSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            update_change_reason(instance, f"{request.user}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_or_create_model(model, field_name, value):
    if not value:
        return None
    obj, created = model.objects.get_or_create(**{field_name: value})
    return obj



class GetTexnologyFromAgent(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        ipadresss = data.get("ipadresss")
        mac_address = data.get("mac_adress")
        print(data)
        if not mac_address or not ipadresss:
            return Response({"error": "IP and MAC address are required"}, status=400)

        with transaction.atomic():
            # Find existing computer by mac_address and ipadresss
            comp = Compyuter.objects.filter(mac_adress=mac_address, ipadresss=ipadresss).first()
            created = False

            if not comp:
                # Create new computer if not found
                comp = Compyuter(mac_adress=mac_address, ipadresss=ipadresss)
                created = True

            # Simple fields
            simple_fields = ["user", "slug", "internet"]
            for field in simple_fields:
                if field in data:
                    setattr(comp, field, data.get(field, None))

            # ForeignKey fields (create if not exists)
            fk_fields = {
                "departament": Department,
                "warehouse_manager": WarehouseManager,
                "type_compyuter": TypeCompyuter,
                "motherboard": Motherboard,
                "motherboard_model": MotherboardModel,
                "CPU": CPU,
                "generation": Generation,
                "frequency": Frequency,
                "HDD": HDD,
                "SSD": SSD,
                "disk_type": DiskType,
                "RAM_type": RAMType,
                "RAMSize": RAMSize,
                "GPU": GPU,
            }

            for field, model in fk_fields.items():
                value = data.get(field)
                if value:
                    obj, _ = model.objects.get_or_create(name=value)
                    setattr(comp, field, obj)
                elif not getattr(comp, field):
                    setattr(comp, field, model.objects.get_or_create(name="Нет")[0])
            # if not comp.slug:
            #     comp.slug = f"computers/{comp.mac_adress}"

            comp.internet = data.get("Internet")
            comp.save()
            # ManyToMany fields (clear and add new)
            m2m_fields = {
                # "printer": Printer,
                # "scaner": Scaner,
                "type_webcamera": TypeWebCamera,
                "model_webcam": ModelWebCamera,
                "type_monitor": Monitor,
            }

            for field, model in m2m_fields.items():
                values = data.get(field, [])
                if isinstance(values, str):
                    values = [values]  # Convert single string to list

                if values:
                    objs = [model.objects.get_or_create(name=value)[0] for value in values]
                    getattr(comp, field).set(objs)

          

        message = "Update successful" if not created else "OK"
        return Response({"message": message, "created": created})


class FilterDataByIPApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, *args, **kwargs):
       
        key = request.data.get('key')

        if key == "Все компьютеры":
     
            computers = Compyuter.objects.all().distinct()

        elif key == "Рабочие компьютеры":

            computers = Compyuter.objects.filter(isActive=True).distinct()

        elif key == "Принтеры":
  
            computers = Compyuter.objects.filter(printer__isnull=False).exclude(printer__name="Нет").distinct()

        elif key == "Сканеры":
            computers = Compyuter.objects.filter(scaner__isnull=False).exclude(scaner__name="Нет").distinct()

        elif key == "МФУ":
            computers = Compyuter.objects.filter(mfo=True).distinct()

        elif key == "Интернет":
            computers = Compyuter.objects.filter(internet=True).distinct()

        elif key == "Веб-камеры":
           
            computers = Compyuter.objects.filter(type_webcamera__isnull=False).exclude(type_webcamera__name="Нет").distinct()

        else:
     
            return Response({"error": "Invalid key value"}, status=400)

        serializer = CompyuterSerializer(computers, many=True)
    
        return Response(serializer.data)


class EditCompyuterApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def put(request, *args, **kwargs):
        instance = get_object_or_404(Compyuter, slug=kwargs.get('slug'))
        serializer = AddCompyuterSerializer(instance, data=request.data)
        if serializer.is_valid():
            update_change_reason(instance, f"{request.user}")
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetDataByIPApiView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def get(request, *args, **kwargs):
        compyuter = get_object_or_404(Compyuter, ipadresss=kwargs.get('ip'))
        serializer = AddCompyuterSerializer(compyuter)
        return Response(serializer.data, status=status.HTTP_200_OK)


def upload_excel(request):
    if request.method == "POST" and request.FILES.get("file"):
        file = request.FILES["file"]
        try:
            import_computers_from_excel(file)
            messages.success(request, "✅ Excel ma'lumotlari yuklandi!")
        except Exception as e:
            messages.error(request, f"❌ Xatolik: {e}")
        return redirect("upload-excel")
    return render(request, "upload.html")



# class GetComputerWithMac(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
    
#     @staticmethod
#     def get(request, *args, **kwargs):
#         mac = getmac.get_mac_address()
#         computer = Compyuter.objects.filter(mac_adress=mac)
#         print(mac, "1111111111")
#         serializer = CompyuterSerializer(computer, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
            
class GetComputerWithMac(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, *args, **kwargs):
        # Foydalanuvchi IP manzilini olish
        ip = request.META.get('REMOTE_ADDR')
       

        # IP orqali MAC olish (Linux yoki Windows uchun)
        import subprocess
        import platform

        if platform.system() == "Windows":
            result = subprocess.run(["arp", "-a"], capture_output=True, text=True)
            mac = None
            for line in result.stdout.splitlines():
                if ip in line:
                    mac = line.split()[1]
                    break
        else:
            result = subprocess.run(["arp", "-n", ip], capture_output=True, text=True)
            mac = result.stdout.split()[3] if result.stdout else None


        # Kompyuter qidirish
        computer = Compyuter.objects.filter(mac_adress=mac)
        serializer = CompyuterSerializer(computer, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
