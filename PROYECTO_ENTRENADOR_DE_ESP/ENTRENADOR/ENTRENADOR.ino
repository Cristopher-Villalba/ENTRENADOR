#include "ThingSpeak.h"
#include <WiFi.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <DHT.h>

// Configuración WiFi y ThingSpeak
const char* ssid = "1234";  
const char* password = "1234";
WiFiClient client;
unsigned long myChannelNumber = 2733749;
const char * myWriteAPIKey = "MM77GAZXG8R70EKB";

// Configuración del temporizador para ThingSpeak
unsigned long lastTime = 0;
unsigned long timerDelay = 1000;

// Configuración del DHT11
#define DHTPIN 4          // Pin del DHT11
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

// Configuración de la pantalla OLED
#define SCREEN_WIDTH 128  // Ancho de la pantalla OLED
#define SCREEN_HEIGHT 64  // Altura de la pantalla OLED
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

// Configuración de la fotocelda
const int ldrPin = 34;  // Pin analógico para la fotocelda (GPIO 34)

void setup() {
  Serial.begin(115200);

  // Configuración de WiFi
  WiFi.mode(WIFI_STA);   
  ThingSpeak.begin(client);

  // Inicializar el sensor DHT11
  dht.begin();

  // Inicializar la pantalla OLED
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { 
    Serial.println(F("OLED no encontrada"));
    while (true);
  }
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);

  // Configuración del pin de la fotocelda
  pinMode(ldrPin, INPUT);
}

void loop() {
  // Si ya pasaron 30 s
  if ((millis() - lastTime) > timerDelay) {
    // Verificar conexión WiFi
    if (WiFi.status() != WL_CONNECTED) {
      Serial.print("Conectando a WiFi");
      while (WiFi.status() != WL_CONNECTED) {
        WiFi.begin(ssid, password); 
        delay(2000);     
      }
      Serial.println("\nConectado a WiFi");
    }

    // Leer la temperatura y la humedad del DHT11
    float temperatura = dht.readTemperature();
    float humedad = dht.readHumidity();

    // Leer el valor de la fotocelda
    int ldrValue = analogRead(ldrPin);

    // Verificar si las lecturas del DHT11 son válidas
    if (isnan(temperatura) || isnan(humedad)) {
      Serial.println("Error leyendo el DHT11");
    } else {
      // Mostrar en el monitor serial
      Serial.print("Temperatura: ");
      Serial.print(temperatura);
      Serial.print("°C  Humedad: ");
      Serial.print(humedad);
      Serial.print("%  Luz: ");
      Serial.println(ldrValue);

      // Mostrar en la pantalla OLED
      display.clearDisplay();
      display.setTextSize(1);
      display.setCursor(0, 20);
      display.print("Temp: ");
      display.print(temperatura);
      display.println(" C");
      display.print("Hum: ");
      display.print(humedad);
      display.println(" %");
      display.print("Luz: ");
      display.print(ldrValue);
      display.display();

      // Enviar los datos a ThingSpeak
      ThingSpeak.setField(1, temperatura);  // Campo 1: Temperatura
      ThingSpeak.setField(2, humedad);      // Campo 2: Humedad
      ThingSpeak.setField(3, ldrValue);     // Campo 3: Luz (Fotocelda)
      int x = ThingSpeak.writeFields(myChannelNumber, myWriteAPIKey);
      if (x == 200) {
        Serial.println("Actualización exitosa en ThingSpeak.");
      } else {
        Serial.println("Error en ThingSpeak: Código HTTP " + String(x));
      }
    }
    lastTime = millis();  // Actualizar el temporizador
  }
}
