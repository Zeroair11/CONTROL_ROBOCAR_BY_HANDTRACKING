#include <WiFi.h>

//================ WIFI =================
const char* ssid = "H29 Coffee and Tea";
const char* password = "29tranhungdao";

//================ TCP SERVER =================
WiFiServer server(1234);

//================ L298N PINS =================
#define IN1 27
#define IN2 26
#define IN3 25
#define IN4 33

#define ENA 14
#define ENB 12

//================ SPEED =================
int motorSpeed = 220;

//================ MOTOR =================
void stopMotor() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
}

void forwardMotor() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
}

void backwardMotor() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
}

void leftMotor() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
}

void rightMotor() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
}

//================ SETUP =================
void setup() {

  Serial.begin(115200);

  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  // ===== PWM (ESP32 CORE v3.x CORRECT WAY) =====
  ledcAttach(ENA, 1000, 8);
  ledcAttach(ENB, 1000, 8);

  ledcWrite(ENA, motorSpeed);
  ledcWrite(ENB, motorSpeed);

  stopMotor();

  //================ WIFI =================
  WiFi.begin(ssid, password);

  Serial.print("Connecting WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi Connected");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());

  //================ SERVER =================
  server.begin();
  Serial.println("TCP Server Started");
}

//================ LOOP =================
void loop() {

  WiFiClient client = server.available();

  if (client) {

    Serial.println("Client Connected");

    while (client.connected()) {

      if (client.available()) {

        char command = client.read();

        Serial.println(command);

        switch (command) {

          case 'F':
            forwardMotor();
            break;

          case 'B':
            backwardMotor();
            break;

          case 'L':
            leftMotor();
            break;

          case 'R':
            rightMotor();
            break;

          case 'S':
          default:
            stopMotor();
            break;
        }
      }
    }

    client.stop();
    stopMotor();

    Serial.println("Client Disconnected");
  }
}