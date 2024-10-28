from django.http import JsonResponse
from rest_framework.decorators import api_view
import cv2
import numpy as np
import torch
from facenet_pytorch import MTCNN, InceptionResnetV1
from admin_web.models import Mahasiswa, PresensiMahasiswa, JadwalKelas, WajahMahasiswa
from torchvision import datasets
from torch.utils.data import DataLoader
from PIL import Image
import os
from django.utils import timezone

mtcnn = MTCNN(keep_all=True, min_face_size=40)
resnet = InceptionResnetV1(pretrained='vggface2').eval()

def get_face_data():
    wajah_mahasiswa = WajahMahasiswa.objects.all()
    embeddings = []
    labels = []
    for wajah in wajah_mahasiswa:
        image_path = wajah.image.path
        if os.path.exists(image_path):
            img = Image.open(image_path).convert('RGB')
            img_cropped, _ = mtcnn(img, return_prob=True)
            if img_cropped is not None:
                for img_tensor in img_cropped:
                    emb = resnet(img_tensor.unsqueeze(0)).detach() 
                    embeddings.append(emb)
                    labels.append(wajah.mahasiswa.id)
    return {'embeddings': embeddings, 'labels': labels}

def recognize_face(face_tensor, embeddings, labels):
    emb = resnet(face_tensor.unsqueeze(0)).detach()
    distances = [torch.dist(emb, emb_db).item() for emb_db in embeddings]
    min_dist = min(distances)
    min_dist_idx = distances.index(min_dist)

    if min_dist < 0.90:
        return labels[min_dist_idx]
    return None

@api_view(['POST'])
def start_attendance(request, jadwal_kelas_id):
    try:
        jadwal_kelas = JadwalKelas.objects.get(id=jadwal_kelas_id)
    except JadwalKelas.DoesNotExist:
        return JsonResponse({'error': 'Jadwal kelas tidak ditemukan'}, status=404)

    face_data = get_face_data()
    embeddings = face_data['embeddings']
    labels = face_data['labels']
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        img_cropped_list, prob_list = mtcnn(img, return_prob=True) 

        if img_cropped_list is not None:
            for i, prob in enumerate(prob_list):
                if prob > 0.90:
                    face_tensor = img_cropped_list[i] 
                    mahasiswa_id = recognize_face(face_tensor, embeddings, labels)
                    if mahasiswa_id:
                        try:
                            presensi = PresensiMahasiswa.objects.get(
                                mahasiswa_id=mahasiswa_id,
                                jadwal_kelas=jadwal_kelas
                            )
                            presensi.status = 'hadir'
                            presensi.tanggal_presensi = timezone.now()
                            presensi.presensi_oleh = 'AI'
                            presensi.save()
                        except PresensiMahasiswa.DoesNotExist:
                            pass

                        mahasiswa = Mahasiswa.objects.get(id=mahasiswa_id)
                        student_name = mahasiswa.nama 
                        box = mtcnn.detect(img)[0][i].astype(int)  
                        cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (255, 0, 0), 2) 

                        cv2.putText(frame, student_name, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        cv2.imshow('Attendance', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break

    cap.release()
    cv2.destroyAllWindows()
    return JsonResponse({'message': 'Presensi selesai'})

@api_view(['GET'])
def list_attendance(request, jadwal_kelas_id):
    presensi_data = PresensiMahasiswa.objects.filter(jadwal_kelas_id=jadwal_kelas_id).select_related('mahasiswa')

    # Cek apakah ada data presensi
    if not presensi_data.exists():
        return JsonResponse({
            'status': 'error',
            'message': 'Data presensi tidak ditemukan untuk jadwal kelas ini.',
            'data': []
        }, status=404)

    # Buat list untuk menampung data hasil query
    data = []
    for presensi in presensi_data:
        mahasiswa = presensi.mahasiswa  # Ambil data mahasiswa dari presensi

        # Tambahkan data presensi ke dalam list
        data.append({
            'nama_mahasiswa': mahasiswa.nama,
            'nim_mahasiswa': mahasiswa.nim,
            'status_presensi': presensi.status,
            'semester_mengambil': mahasiswa.semester,
        })

    return JsonResponse({
        'status': 'success',
        'message': 'Data presensi berhasil ditemukan.',
        'data': data
    }, status=200)