# Architektur-Prinzipien für Webprojekte

**Datum:** 2. Dezember 2025  
**Zielgruppe:** Schüler & Auszubildende  
**Zweck:** Verständliche Einführung in professionelle Software-Architektur

---

## 🎯 Warum sind Architektur-Prinzipien wichtig?

Stell dir vor, du baust ein Haus ohne Plan: Räume sind chaotisch angeordnet, Türen passen nicht, und nach einem Jahr kannst du nichts mehr ändern, ohne alles abzureißen. **Genau so ist es mit Code!**

Gute Architektur bedeutet:

- ✅ Du findest dich auch nach Monaten noch zurecht
- ✅ Andere können deinen Code verstehen und erweitern
- ✅ Fehler lassen sich schnell finden und beheben
- ✅ Neue Features einzubauen ist einfach

---

## 📚 Die 7 Architektur-Prinzipien

### 1. 🧩 Abstraktion

**Was bedeutet das?**  
Verstecke komplexe Details hinter einfachen Schnittstellen. Nutzer müssen nicht wissen, _wie_ etwas funktioniert – nur _was_ es tut.

**Beispiel aus dem Alltag:**  
Du drückst den Lichtschalter, ohne zu wissen, wie Elektrizität funktioniert. Der Schalter ist die _Abstraktion_ für ein komplexes System.

**Code-Beispiel (schlecht):**

```javascript
// ❌ Alle Details sind sichtbar und durcheinander
function displayUserInfo() {
  let firstName = document.getElementById("fname").value;
  let lastName = document.getElementById("lname").value;
  let email = document.getElementById("email").value;

  // Validierung direkt im Display-Code
  if (email.indexOf("@") === -1) {
    alert("Ungültige E-Mail!");
    return;
  }

  // Formatierung direkt hier
  let fullName = firstName.toUpperCase() + " " + lastName.toUpperCase();

  // Ausgabe direkt hier
  document.getElementById("output").innerHTML = fullName + "<br>" + email;
}
```

**Code-Beispiel (gut):**

```javascript
// ✅ Jede Funktion hat eine klare, abstrakte Aufgabe
class User {
  constructor(firstName, lastName, email) {
    this.firstName = firstName;
    this.lastName = lastName;
    this.email = email;
  }

  // Abstraktion: Details der Validierung sind versteckt
  isValid() {
    return (
      this.email.includes("@") &&
      this.firstName.length > 0 &&
      this.lastName.length > 0
    );
  }

  // Abstraktion: Formatierung ist eine eigene Verantwortung
  getFullName() {
    return `${this.firstName} ${this.lastName}`;
  }
}

class UserDisplay {
  // Einfache Schnittstelle: Nutzer übergeben, fertig!
  static show(user) {
    if (!user.isValid()) {
      this.showError("Bitte alle Felder korrekt ausfüllen");
      return;
    }

    document.getElementById("output").innerHTML = `
            <h2>${user.getFullName()}</h2>
            <p>${user.email}</p>
        `;
  }

  static showError(message) {
    document.getElementById("output").innerHTML =
      `<p class="error">${message}</p>`;
  }
}

// Verwendung: Super einfach!
let user = new User("Max", "Mustermann", "max@example.com");
UserDisplay.show(user);
```

**In diesem Projekt:**

- `version2/loesung/js/script.js` nutzt Funktionen wie `initMobileMenu()` – du musst nicht wissen, wie das Menü intern funktioniert
- CSS-Klassen wie `.btn-primary` abstrahieren komplexe Styles

---

### 2. ♻️ Wiederverwendbarkeit

**Was bedeutet das?**  
Schreibe Code einmal und nutze ihn an vielen Stellen – statt Copy & Paste!

**Beispiel aus dem Alltag:**  
LEGO-Steine! Du baust nicht für jedes Modell neue Steine, sondern verwendest die gleichen Bausteine immer wieder.

**Code-Beispiel (schlecht):**

```css
/* ❌ Gleicher Code wird immer wieder wiederholt */
.button-home {
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border-radius: 5px;
  border: none;
  cursor: pointer;
}

.button-contact {
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border-radius: 5px;
  border: none;
  cursor: pointer;
}

.button-submit {
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border-radius: 5px;
  border: none;
  cursor: pointer;
}
```

**Code-Beispiel (gut):**

```css
/* ✅ Einmal definiert, überall nutzbar */
.btn {
  padding: 10px 20px;
  border-radius: 5px;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn-large {
  padding: 15px 30px;
  font-size: 1.2rem;
}
```

```html
<!-- Verwendung: Kombiniere Klassen nach Bedarf -->
<button class="btn btn-primary">Absenden</button>
<button class="btn btn-secondary">Abbrechen</button>
<button class="btn btn-primary btn-large">Jetzt starten!</button>
```

**JavaScript-Beispiel:**

```javascript
// ✅ Wiederverwendbare Hilfsfunktion
function formatDate(date) {
  const options = { year: "numeric", month: "long", day: "numeric" };
  return date.toLocaleDateString("de-DE", options);
}

// Überall im Code verwendbar
console.log(formatDate(new Date())); // "2. Dezember 2025"
document.getElementById("date1").textContent = formatDate(someDate);
document.getElementById("date2").textContent = formatDate(anotherDate);
```

**In diesem Projekt:**

- `shared-examples/css/style.css` enthält wiederverwendbare CSS-Komponenten
- Die `templates/` enthalten vorgefertigte, wiederverwendbare Layouts

---

### 3. 🔨 Zerlegung (Modularität)

**Was bedeutet das?**  
Teile große Probleme in viele kleine, überschaubare Teile auf. Jedes Teil hat genau eine Aufgabe.

**Beispiel aus dem Alltag:**  
Ein Auto besteht aus Motor, Bremsen, Lenkung usw. Wenn die Bremse kaputt ist, tauschst du nur die Bremse aus – nicht das ganze Auto!

**Code-Beispiel (schlecht):**

```javascript
// ❌ Eine Mega-Funktion macht ALLES
function handleEverything() {
  // Daten aus Formular holen
  let name = document.getElementById("name").value;
  let email = document.getElementById("email").value;

  // Validieren
  if (name === "" || email === "") {
    alert("Fehler!");
    return;
  }

  // Speichern
  localStorage.setItem("user", JSON.stringify({ name, email }));

  // API-Call
  fetch("/api/users", {
    method: "POST",
    body: JSON.stringify({ name, email }),
  });

  // UI aktualisieren
  document.getElementById("welcome").textContent = "Hallo " + name;

  // Statistik
  let count = parseInt(localStorage.getItem("userCount") || "0");
  localStorage.setItem("userCount", count + 1);
}
```

**Code-Beispiel (gut):**

```javascript
// ✅ Jede Funktion hat EINE klare Aufgabe

// Modul 1: Daten sammeln
function getFormData() {
  return {
    name: document.getElementById("name").value,
    email: document.getElementById("email").value,
  };
}

// Modul 2: Validierung
function validateUser(user) {
  if (!user.name || !user.email) {
    throw new Error("Name und E-Mail sind erforderlich");
  }
  if (!user.email.includes("@")) {
    throw new Error("Ungültige E-Mail-Adresse");
  }
  return true;
}

// Modul 3: Lokale Speicherung
function saveUserLocally(user) {
  localStorage.setItem("user", JSON.stringify(user));
  incrementUserCount();
}

function incrementUserCount() {
  let count = parseInt(localStorage.getItem("userCount") || "0");
  localStorage.setItem("userCount", count + 1);
}

// Modul 4: API-Kommunikation
async function saveUserToServer(user) {
  const response = await fetch("/api/users", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(user),
  });
  return response.json();
}

// Modul 5: UI-Updates
function showWelcomeMessage(name) {
  document.getElementById("welcome").textContent = `Hallo ${name}`;
}

function showError(message) {
  alert(message);
}

// Orchestrierung: Kombiniert die Module
async function handleUserRegistration() {
  try {
    const user = getFormData();
    validateUser(user);
    saveUserLocally(user);
    await saveUserToServer(user);
    showWelcomeMessage(user.name);
  } catch (error) {
    showError(error.message);
  }
}
```

**HTML-Zerlegung:**

```html
<!-- ✅ Struktur in logische Bereiche zerlegt -->
<body>
  <header><!-- Navigation & Logo --></header>

  <main>
    <section id="hero"><!-- Startbereich --></section>
    <section id="features"><!-- Feature-Liste --></section>
    <section id="contact"><!-- Kontaktformular --></section>
  </main>

  <footer><!-- Copyright & Links --></footer>
</body>
```

**In diesem Projekt:**

- Ordnerstruktur: `css/`, `js/`, `images/` – jeder Dateityp an seinem Platz
- `version3/aufgabe/phase1-concept/` und `phase2-implementation/` – Phasen sind getrennt

---

### 4. 🚀 Erweiterbarkeit

**Was bedeutet das?**  
Code so schreiben, dass neue Features leicht hinzugefügt werden können – ohne alles umzuschreiben.

**Beispiel aus dem Alltag:**  
Ein Smartphone mit App Store! Du kannst jederzeit neue Apps installieren, ohne das Betriebssystem neu zu programmieren.

**Code-Beispiel (schlecht):**

```javascript
// ❌ Für jeden neuen Button-Typ muss der Code geändert werden
function createButton(type, text) {
  let button = document.createElement("button");
  button.textContent = text;

  if (type === "primary") {
    button.style.backgroundColor = "#007bff";
    button.style.color = "white";
  } else if (type === "secondary") {
    button.style.backgroundColor = "#6c757d";
    button.style.color = "white";
  } else if (type === "danger") {
    button.style.backgroundColor = "#dc3545";
    button.style.color = "white";
  }
  // Für jeden neuen Typ: else if hinzufügen! 😫

  return button;
}
```

**Code-Beispiel (gut):**

```javascript
// ✅ Neue Button-Typen können einfach hinzugefügt werden
const BUTTON_STYLES = {
  primary: {
    backgroundColor: "#007bff",
    color: "white",
    hoverColor: "#0056b3",
  },
  secondary: {
    backgroundColor: "#6c757d",
    color: "white",
    hoverColor: "#545b62",
  },
  danger: {
    backgroundColor: "#dc3545",
    color: "white",
    hoverColor: "#c82333",
  },
  // Neuer Typ? Einfach hier hinzufügen! 😊
  success: {
    backgroundColor: "#28a745",
    color: "white",
    hoverColor: "#218838",
  },
};

class Button {
  constructor(type, text) {
    this.type = type;
    this.text = text;
    this.element = this.create();
  }

  create() {
    const btn = document.createElement("button");
    btn.textContent = this.text;
    btn.className = `btn btn-${this.type}`;

    const styles = BUTTON_STYLES[this.type];
    if (styles) {
      Object.assign(btn.style, styles);
    }

    return btn;
  }

  // Erweiterbar: Neue Methoden können hinzugefügt werden
  onClick(callback) {
    this.element.addEventListener("click", callback);
    return this; // Method Chaining
  }

  disable() {
    this.element.disabled = true;
    return this;
  }
}

// Verwendung
const saveBtn = new Button("primary", "Speichern").onClick(() =>
  console.log("Gespeichert!"),
);
```

**CSS-Erweiterbarkeit:**

```css
/* ✅ CSS Custom Properties (Variablen) ermöglichen einfache Anpassungen */
:root {
  --color-primary: #007bff;
  --color-secondary: #6c757d;
  --color-success: #28a745;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
}

.card {
  padding: var(--spacing-md);
  border: 1px solid var(--color-primary);
}

/* Neue Variante? Einfach Variable überschreiben! */
.card-large {
  padding: var(--spacing-lg);
}
```

**In diesem Projekt:**

- `version1/`, `version2/`, `version3/` – neue Versionen werden hinzugefügt, ohne alte zu ändern
- `templates/` – neue Templates können jederzeit ergänzt werden

---

### 5. 🔒 Sicherheit

**Was bedeutet das?**  
Schütze deine Anwendung vor Angriffen und Datenverlust. Vertraue niemals Benutzereingaben!

**Beispiel aus dem Alltag:**  
Du lässt nicht jeden in dein Haus, nur weil er klingelt. Du prüfst erst, wer da ist!

**Häufige Sicherheitsprobleme:**

#### 1. XSS (Cross-Site Scripting)

```javascript
// ❌ GEFÄHRLICH: Benutzereingabe direkt ins HTML
function displayComment(comment) {
  document.getElementById("comments").innerHTML = comment;
  // Wenn comment = "<script>alert('Gehackt!')</script>", wird es ausgeführt! 😱
}

// ✅ SICHER: Text escapen
function displayCommentSafe(comment) {
  const div = document.createElement("div");
  div.textContent = comment; // textContent escaped automatisch
  document.getElementById("comments").appendChild(div);
}

// ✅ SICHER: Mit DOMPurify-Bibliothek
function displayCommentWithHTML(comment) {
  const clean = DOMPurify.sanitize(comment);
  document.getElementById("comments").innerHTML = clean;
}
```

#### 2. Eingabevalidierung

```javascript
// ❌ Nur Frontend-Validierung = UNSICHER
function submitForm(data) {
  if (data.email.includes("@")) {
    // Direkt senden – Angreifer können Frontend umgehen!
    sendToServer(data);
  }
}

// ✅ Frontend UND Backend validieren
// Frontend (User Experience):
function validateEmail(email) {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
}

// Backend (PHP-Beispiel – MUSS sein!):
/*
<?php
$email = $_POST['email'];
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    die('Ungültige E-Mail');
}
// Nur validierte Daten weiterverarbeiten
?>
*/
```

#### 3. Sensible Daten schützen

```javascript
// ❌ NIEMALS Passwörter oder API-Keys im Frontend!
const API_KEY = "sk_live_123456789"; // Jeder kann das sehen! 😱

// ✅ Umgebungsvariablen nutzen (Backend)
// .env Datei (NICHT committen!):
// API_KEY=sk_live_123456789

// Backend holt den Key:
const apiKey = process.env.API_KEY;

// Frontend bekommt nur sichere Endpoints:
fetch("/api/data"); // Backend nutzt intern den API_KEY
```

#### 4. SQL-Injection verhindern

```php
<!-- ❌ GEFÄHRLICH: Direkte String-Konkatenation -->
<?php
$user = $_GET['username'];
$sql = "SELECT * FROM users WHERE username = '$user'";
// Angreifer sendet: admin' OR '1'='1
// SQL wird zu: SELECT * FROM users WHERE username = 'admin' OR '1'='1'
// = Alle Nutzer werden zurückgegeben! 😱
?>

<!-- ✅ SICHER: Prepared Statements -->
<?php
$stmt = $pdo->prepare("SELECT * FROM users WHERE username = ?");
$stmt->execute([$user]);
// Eingabe wird automatisch escaped
?>
```

**In diesem Projekt:**

- `.gitignore` verhindert, dass sensible Dateien committed werden
- Formulare in `docs/formulare.md` zeigen sichere Validierung
- Keine Passwörter oder API-Keys im Code

**Sicherheits-Checkliste:**

- [ ] Benutzereingaben immer validieren (Frontend + Backend)
- [ ] Niemals `innerHTML` mit Benutzerdaten verwenden
- [ ] Sensible Daten nie im Frontend speichern
- [ ] HTTPS verwenden (in Produktion)
- [ ] `.gitignore` für Secrets nutzen
- [ ] Prepared Statements für Datenbanken

---

### 6. 🔧 Wartbarkeit

**Was bedeutet das?**  
Code so schreiben, dass du (und andere) ihn auch nach Monaten noch verstehst und ändern kannst.

**Beispiel aus dem Alltag:**  
Ein gut beschrifteter Werkzeugkasten vs. eine Kiste mit durcheinander geworfenen Werkzeugen!

#### 1. Sprechende Namen

```javascript
// ❌ Schlecht: Kryptische Namen
function calc(a, b) {
  let x = a * 0.19;
  let y = a + x;
  return y - b;
}
let z = calc(100, 10);

// ✅ Gut: Namen erklären die Bedeutung
function calculateTotalPrice(netPrice, discount) {
  const taxAmount = netPrice * 0.19; // 19% MwSt
  const grossPrice = netPrice + taxAmount;
  const finalPrice = grossPrice - discount;
  return finalPrice;
}
const totalPrice = calculateTotalPrice(100, 10);
```

#### 2. Kommentare (wo sinnvoll)

```javascript
// ❌ Überflüssige Kommentare
let i = 0; // Setze i auf 0
i++; // Erhöhe i um 1

// ✅ Nützliche Kommentare
// Berechne Rabatt basierend auf Kundenkategorie (Business-Logik von 2024)
const discount = customer.isPremium ? price * 0.15 : price * 0.05;

// WORKAROUND: Safari < 15 unterstützt kein 'gap' in Flexbox
// TODO: Entfernen, sobald Safari 15+ Mindestversion ist (Q2 2026)
.flex-container > * {
    margin-right: 10px;
}
```

#### 3. Konsistenter Code-Stil

```javascript
// ❌ Inkonsistent und chaotisch
function getData() {
  let Name = "Max";
  const age = 25;
  return { name: Name, age: age };
}

// ✅ Konsistent formatiert
function getData() {
  const name = "Max";
  const age = 25;
  return { name, age };
}
```

#### 4. Dateiorganisation

```
✅ Gute Struktur:
project/
├── index.html
├── css/
│   ├── style.css          # Haupt-Styles
│   ├── components.css     # Wiederverwendbare Komponenten
│   └── responsive.css     # Media Queries
├── js/
│   ├── main.js           # Entry Point
│   ├── utils.js          # Hilfsfunktionen
│   └── api.js            # API-Calls
└── images/
    ├── logo.svg
    └── hero.jpg

❌ Schlechte Struktur:
project/
├── index.html
├── file1.css
├── script-final-v2-copy.js
├── test123.js
└── img_20241201_old.jpg
```

#### 5. README und Dokumentation

```markdown
✅ Gute README:

# Mein Projekt

## Installation

npm install

## Entwicklung starten

npm run dev

## Projekt-Struktur

- `src/components/` - React-Komponenten
- `src/utils/` - Hilfsfunktionen
- `public/` - Statische Assets

## Wichtige Entscheidungen

- Wir nutzen Flexbox statt Grid, weil besserer Browser-Support für IE11
- API-Calls laufen über `api.js` für zentrale Error-Handling
```

**In diesem Projekt:**

- Jede Version hat eine eigene `README.md` mit klaren Anweisungen
- `docs/` enthält umfangreiche Dokumentation
- Konsistente Ordnerstruktur (`css/`, `js/`, `images/`)
- Scripts in `scripts/` haben beschreibende Namen

**Wartbarkeits-Checkliste:**

- [ ] Sprechende Variablen- und Funktionsnamen
- [ ] Kommentare für komplexe Logik
- [ ] Konsistente Formatierung (Prettier/ESLint nutzen)
- [ ] README mit Installationsanleitung
- [ ] Logische Ordnerstruktur

---

### 7. 🏛️ MVC-Architektur (Model-View-Controller)

**Was bedeutet das?**  
Trenne Daten, Darstellung und Logik – so bleibt alles übersichtlich!

**Beispiel aus dem Alltag:**  
Restaurant: Koch (Controller) nimmt Bestellung entgegen, bereitet Essen (Model) zu, und Kellner (View) serviert es dem Gast.

#### Die drei Schichten:

```
┌─────────────────────────────────────┐
│         VIEW (Darstellung)          │
│   Was der Nutzer sieht & bedient    │
│        HTML, CSS, Templates         │
└──────────────┬──────────────────────┘
               │
               ↕ Nutzer-Interaktionen
               │
┌──────────────┴──────────────────────┐
│      CONTROLLER (Steuerung)         │
│  Reagiert auf Events, koordiniert   │
│      JavaScript Event Handler       │
└──────────────┬──────────────────────┘
               │
               ↕ Daten abrufen/ändern
               │
┌──────────────┴──────────────────────┐
│         MODEL (Daten)               │
│    Business-Logik, Datenstruktur    │
│   JavaScript-Klassen, API-Calls     │
└─────────────────────────────────────┘
```

#### Beispiel: Todo-Liste

**❌ Ohne MVC (alles durcheinander):**

```javascript
// Alles in einer Datei, keine Trennung
function addTodo() {
  let text = document.getElementById("input").value;

  // Daten & Validierung (sollte MODEL sein)
  if (text.length < 3) {
    alert("Zu kurz!");
    return;
  }

  // Speichern (sollte MODEL sein)
  let todos = JSON.parse(localStorage.getItem("todos") || "[]");
  todos.push({ id: Date.now(), text: text, done: false });
  localStorage.setItem("todos", JSON.stringify(todos));

  // Darstellung (sollte VIEW sein)
  let li = document.createElement("li");
  li.innerHTML = text + '<button onclick="deleteTodo()">X</button>';
  document.getElementById("list").appendChild(li);
}
```

**✅ Mit MVC (sauber getrennt):**

```javascript
// ============= MODEL (todo-model.js) =============
// Daten und Business-Logik
class TodoModel {
  constructor() {
    this.todos = this.loadFromStorage();
  }

  loadFromStorage() {
    return JSON.parse(localStorage.getItem("todos") || "[]");
  }

  saveToStorage() {
    localStorage.setItem("todos", JSON.stringify(this.todos));
  }

  add(text) {
    if (text.length < 3) {
      throw new Error("Todo muss mindestens 3 Zeichen lang sein");
    }

    const todo = {
      id: Date.now(),
      text: text,
      done: false,
      createdAt: new Date(),
    };

    this.todos.push(todo);
    this.saveToStorage();
    return todo;
  }

  delete(id) {
    this.todos = this.todos.filter((t) => t.id !== id);
    this.saveToStorage();
  }

  toggle(id) {
    const todo = this.todos.find((t) => t.id === id);
    if (todo) {
      todo.done = !todo.done;
      this.saveToStorage();
    }
  }

  getAll() {
    return this.todos;
  }
}

// ============= VIEW (todo-view.js) =============
// Darstellung und UI
class TodoView {
  constructor() {
    this.input = document.getElementById("todo-input");
    this.list = document.getElementById("todo-list");
    this.addBtn = document.getElementById("add-btn");
  }

  renderTodos(todos) {
    this.list.innerHTML = ""; // Liste leeren

    todos.forEach((todo) => {
      const li = this.createTodoElement(todo);
      this.list.appendChild(li);
    });
  }

  createTodoElement(todo) {
    const li = document.createElement("li");
    li.className = todo.done ? "todo-item done" : "todo-item";
    li.dataset.id = todo.id;

    li.innerHTML = `
            <input type="checkbox" ${todo.done ? "checked" : ""}>
            <span>${todo.text}</span>
            <button class="delete-btn">×</button>
        `;

    return li;
  }

  getInputValue() {
    return this.input.value.trim();
  }

  clearInput() {
    this.input.value = "";
  }

  showError(message) {
    alert(message); // In echten Apps: Toast/Modal verwenden
  }
}

// ============= CONTROLLER (todo-controller.js) =============
// Koordiniert Model und View
class TodoController {
  constructor(model, view) {
    this.model = model;
    this.view = view;

    // Event Listener registrieren
    this.view.addBtn.addEventListener("click", () => this.handleAdd());
    this.view.list.addEventListener("click", (e) => this.handleListClick(e));

    // Initial rendern
    this.updateView();
  }

  handleAdd() {
    const text = this.view.getInputValue();

    try {
      this.model.add(text);
      this.view.clearInput();
      this.updateView();
    } catch (error) {
      this.view.showError(error.message);
    }
  }

  handleListClick(event) {
    const todoItem = event.target.closest(".todo-item");
    if (!todoItem) return;

    const id = parseInt(todoItem.dataset.id);

    if (event.target.type === "checkbox") {
      this.model.toggle(id);
      this.updateView();
    } else if (event.target.classList.contains("delete-btn")) {
      this.model.delete(id);
      this.updateView();
    }
  }

  updateView() {
    const todos = this.model.getAll();
    this.view.renderTodos(todos);
  }
}

// ============= INITIALISIERUNG (main.js) =============
// App starten
const model = new TodoModel();
const view = new TodoView();
const controller = new TodoController(model, view);
```

**HTML für das Beispiel:**

```html
<!DOCTYPE html>
<html lang="de">
  <head>
    <meta charset="UTF-8" />
    <title>Todo MVC</title>
    <link rel="stylesheet" href="style.css" />
  </head>
  <body>
    <div class="container">
      <h1>Meine Todos</h1>

      <!-- VIEW: Eingabebereich -->
      <div class="input-group">
        <input type="text" id="todo-input" placeholder="Neue Aufgabe..." />
        <button id="add-btn">Hinzufügen</button>
      </div>

      <!-- VIEW: Todo-Liste -->
      <ul id="todo-list"></ul>
    </div>

    <!-- Skripte in richtiger Reihenfolge -->
    <script src="todo-model.js"></script>
    <script src="todo-view.js"></script>
    <script src="todo-controller.js"></script>
    <script src="main.js"></script>
  </body>
</html>
```

#### Vorteile von MVC:

✅ **Änderungen sind isoliert:**

- Neue Darstellung? Nur VIEW ändern
- Andere Speicher-Methode? Nur MODEL ändern
- Neue Funktionen? Controller erweitern

✅ **Testbar:**

- Model kann ohne UI getestet werden
- View kann mit Mock-Daten getestet werden

✅ **Teamarbeit:**

- Designer arbeitet an VIEW
- Backend-Entwickler an MODEL
- Frontend-Entwickler an CONTROLLER

**In diesem Projekt:**

- `version2/loesung/` zeigt Trennung von HTML (View), CSS (View-Styling), JS (Controller)
- Templates in `templates/` folgen MVC-Prinzipien
- `docs/react.md` erklärt komponentenbasierte Architektur (moderne MVC-Variante)

---

## 🎯 Zusammenfassung: Die Prinzipien in der Praxis

### Checkliste für deine Projekte

Bevor du Code committed, frage dich:

- [ ] **Abstraktion**: Sind komplexe Details hinter einfachen Schnittstellen versteckt?
- [ ] **Wiederverwendbarkeit**: Habe ich Code kopiert, den ich in Funktionen/Klassen auslagern könnte?
- [ ] **Zerlegung**: Sind meine Funktionen klein und fokussiert (max. 20 Zeilen)?
- [ ] **Erweiterbarkeit**: Könnte ich leicht neue Features hinzufügen ohne alles umzuschreiben?
- [ ] **Sicherheit**: Habe ich Benutzereingaben validiert? Sind sensible Daten geschützt?
- [ ] **Wartbarkeit**: Würde ich meinen Code in 6 Monaten noch verstehen?
- [ ] **MVC**: Sind Daten, Darstellung und Logik getrennt?

### Lern-Roadmap

1. **Anfänger**: Fokus auf Wartbarkeit (gute Namen, Kommentare, Struktur)
2. **Fortgeschritten**: Wiederverwendbarkeit und Zerlegung (Funktionen, Klassen)
3. **Profi**: MVC, Abstraktion, Erweiterbarkeit (Design Patterns)

---

## 📚 Weitere Ressourcen

- [`docs/handbook/ARCHITECTURE.md`](ARCHITECTURE.md) – Technische Validierung für Lehrende
- [`CONTRIBUTING.md`](../../CONTRIBUTING.md) – Workflow & Git-Best-Practices
- [`docs/konzeption/git-versionsmanagement.md`](../konzeption/git-versionsmanagement.md) – Git-Grundlagen
- [`docs/dynamisch/testen.md`](../dynamisch/testen.md) – Code-Tests schreiben

---

## ❓ Fragen?

Wenn du dir bei einer Architektur-Entscheidung unsicher bist:

1. **Frag dich:** "Würde ich das in 6 Monaten noch verstehen?"
2. **Denk an KISS:** Keep It Simple, Stupid – einfache Lösungen sind oft die besten
3. **Code Review:** Lass andere drüberschauen
4. **Refactoring:** Code muss nicht beim ersten Mal perfekt sein – verbessere ihn schrittweise!

**Happy Coding! 🚀**
