# HTTP Server Projesi

Bu proje, Bilgisayar Ağları/Sistem Programlama dersi kapsamında geliştirilmiş, sıfırdan yazılmış basit bir HTTP sunucusudur. Python dilinde socket programlama kullanılmıştır. Amaç, temel HTTP protokolü mantığını, MIME tipi yönetimini ve containerization kavramlarını deneyimlemektir.

## Özellikler

- `GET` isteklerini destekler
- `/static` dizininden HTML dosyası sunar
- `/api/hello` endpoint'i JSON döner
- MIME türü doğru tanımlanır
- Türkçe karakter sorunu çözülmüştür (`charset=utf-8`)
- Loglama ve volume desteği eklenmiştir
- Docker ve docker-compose desteği mevcuttur

## Kullanım

```bash
docker build -t http-server .
docker run -p 8080:8080 http-server
veya
docker compose up -d
