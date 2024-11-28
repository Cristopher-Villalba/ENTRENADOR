# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 10:14:51 2024

@author: crist
"""

import streamlit as st
from PIL import Image


def main():
    st.title("Entrenador ESP32")
    st.subheader('Hola, si quieres aprender a crear tu propio entrenador para ESP32 estás en la pagina indicada.')
    st.write('Para el diseño del PCB se utiliza EasyEDA, un software que permite organizar de forma eficiente el layout del circuito. En este proceso, la pantalla OLED se conecta al ESP32 mediante el protocolo I2C, mientras que los sensores se enlazan a pines analógicos y digitales. Tras diseñar el circuito, se fabrica la baquela y se ensamblan los componentes con soldadura, obteniendo un sistema robusto ideal para aplicaciones en hogares, agricultura y educación. El prototipo está diseñado para medir y mostrar, en tiempo real, la intensidad de luz y la temperatura ambiental. Su enfoque económico y portátil lo convierte en una solución práctica para monitorear estas variables sin depender de dispositivos externos. Su diseño compacto y adaptable lo hace ideal para optimizar recursos como iluminación y climatización en una amplia variedad de entornos. ')
    st.header('Los componetes que se usaron fueron:')
    st.subheader('ESP32-wroom-32 tipo c')
    img = Image.open(r'C:\Users\crist\OneDrive\Escritorio\PYTHON_DIGITALES\IMAGENES_ENTRENADOR\Placa-de-desarrollo-ESP32-WROOM-32-m-dulo-inal-mbrico-de-32Mbits-5V-TYPE-C-CH340C.png')
    new_size = (400, 400)  
    img_resized = img.resize(new_size)
    st.image(img_resized)
    
    st.subheader('Módulo dht11')
    img = Image.open(r'C:\Users\crist\OneDrive\Escritorio\PYTHON_DIGITALES\IMAGENES_ENTRENADOR\images.jpg')
    new_size = (200, 200)  
    img_resized = img.resize(new_size)
    st.image(img_resized)
    
    st.subheader('Fotoresistencia')
    img = Image.open(r'C:\Users\crist\OneDrive\Escritorio\PYTHON_DIGITALES\IMAGENES_ENTRENADOR\fotoresistencia.jpg')
    new_size = (400, 200)  
    img_resized = img.resize(new_size)
    st.image(img_resized)
    
    st.subheader('Resistencia 10K ohm')
    img = Image.open(r'C:\Users\crist\OneDrive\Escritorio\PYTHON_DIGITALES\IMAGENES_ENTRENADOR\10K-1.jpg.png')
    new_size = (400, 200)  
    img_resized = img.resize(new_size)
    st.image(img_resized)

    st.subheader('Regleta de pines hembra')
    img = Image.open(r'C:\Users\crist\OneDrive\Escritorio\PYTHON_DIGITALES\IMAGENES_ENTRENADOR\Regleta-Conector-Hembra-2.54mm-40x1-pines-zamux.jpg')
    new_size = (400, 200)  
    img_resized = img.resize(new_size)
    st.image(img_resized)
    
    st.subheader('Regleta de pines macho')
    img = Image.open(r'C:\Users\crist\OneDrive\Escritorio\PYTHON_DIGITALES\IMAGENES_ENTRENADOR\Regleta-Conector-Macho-2.54mm-40-x-1-pines.jpg')
    new_size = (300, 200)  
    img_resized = img.resize(new_size)
    st.image(img_resized)
    
    st.subheader('Regulador 7805')
    img = Image.open(r'C:\Users\crist\OneDrive\Escritorio\PYTHON_DIGITALES\IMAGENES_ENTRENADOR\D_NQ_NP_976264-MCO46207285304_052021-O.jpg')
    new_size = (300, 200)  
    img_resized = img.resize(new_size)
    st.image(img_resized)
    
    st.subheader('Baquela virgen 10x10 cm')
    img = Image.open(r'C:\Users\crist\OneDrive\Escritorio\PYTHON_DIGITALES\IMAGENES_ENTRENADOR\placa-pcb-virgen-pertinax-experimental-15x20-simple-faz-ptec-D_NQ_NP_625979-MLA26701047790_012018-F.jpg')
    new_size = (300, 200)  
    img_resized = img.resize(new_size)
    st.image(img_resized)
    
    st.header("A continuación te voy a presentar una imagen del esquematico creado en EasyEDA")
    img = Image.open(r'C:\Users\crist\OneDrive\Escritorio\PYTHON_DIGITALES\IMAGENES_ENTRENADOR\ESQUEMATICO.jpg')
    st.image(img, use_column_width=True)
    
    st.info("Para que tu entrenador funcione de la mejor manera usa 2 baterias de 3.7V.")
    img = Image.open(r'C:\Users\crist\OneDrive\Escritorio\PYTHON_DIGITALES\IMAGENES_ENTRENADOR\BATERIA_3.7.jpg')
    new_size = (300, 300)  
    img_resized = img.resize(new_size)
    st.image(img_resized)
    
    st.subheader("Codigo del entrenador:")
    arduino_code ="""
    #include <Adafruit_GFX.h>
    #include <Adafruit_SSD1306.h>
    #include <DHT.h>

    // Configuración WiFi y ThingSpeak
    const char* ssid = "1234";  
    const char* password = "1234";
    WiFiClient client;
    unsigned long myChannelNumber = 1234;
    const char * myWriteAPIKey = "1234";
    
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
    
    """
    st.code(arduino_code, language='cpp')
    st.success("Gracias por ver mi pagina web, espero te sirva tu entrenador.")
    
if __name__ == '__main__' :
    main()