from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# ---------------- FOOD MENU ----------------

foods = [
    {"id": 1, "name": "Veg Sandwich", "price": 60,
     "category": "healthy", "emoji": "🥪"},
    {"id": 2, "name": "Veg Burger", "price": 80,
     "category": "snack", "emoji": "🍔"},
    {"id": 3, "name": "Masala Dosa", "price": 70,
     "category": "spicy", "emoji": "🥞"},
    {"id": 4, "name": "Fruit Bowl", "price": 90,
     "category": "healthy", "emoji": "🍓"},
    {"id": 5, "name": "Samosa", "price": 20,
     "category": "spicy", "emoji": "🥟"},
    {"id": 6, "name": "Chocolate Cake", "price": 50,
     "category": "sweet", "emoji": "🍰"},
    {"id": 7, "name": "French Fries", "price": 60,
     "category": "snack", "emoji": "🍟"},
    {"id": 8, "name": "Fruit Juice", "price": 40,
     "category": "healthy", "emoji": "🧃"}
]

# ---------------- WEBSITE ----------------

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Cafeteria Management System</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: Arial;
            margin: 0;
            background: #fff8ef;
            color: #333;
        }
        header {
            background: #603626;
            color: white;
            padding: 22px;
            text-align: center;
        }
        nav a {
            color: white;
            margin: 10px;
            text-decoration: none;
        }
        section {
            padding: 25px;
            text-align: center;
        }
        .hero {
            background: #f3ddc0;
            padding: 45px 15px;
        }
        .menu {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
            gap: 15px;
        }
        .card {
            background: white;
            border-radius: 12px;
            padding: 18px;
            box-shadow: 0 2px 8px #0002;
        }
        .emoji {
            font-size: 38px;
        }
        button {
            background: #995237;
            color: white;
            padding: 10px 14px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            margin: 5px;
        }
        button:hover {
            background: #603626;
        }
        input, select {
            padding: 10px;
            margin: 6px;
            max-width: 95%;
        }
        .result {
            background: #f3e7d9;
            padding: 12px;
            margin: 12px auto;
            max-width: 600px;
            border-radius: 8px;
        }
        footer {
            background: #603626;
            color: white;
            padding: 15px;
            text-align: center;
        }
    </style>
</head>
<body>

<header>
    <h1>☕ Smart Cafe</h1>
    <p>AI-Based Cafeteria Management System</p>
    <nav>
        <a href="#home">Home</a>
        <a href="#menu">Menu</a>
        <a href="#ai">AI Recommendation</a>
        <a href="#cart">My Order</a>
        <a href="#admin">Admin</a>
    </nav>
</header>

<section class="hero" id="home">
    <h2>Welcome to Smart Cafe!</h2>
    <p>Choose your favourite food and get smart recommendations.</p>
    <a href="#menu"><button>Explore Menu</button></a>
</section>

<section id="menu">
    <h2>🍽️ Our Food Menu</h2>
    <div id="foodMenu" class="menu">Loading menu...</div>
</section>

<section id="ai">
    <h2>🤖 AI Food Recommendation</h2>
    <p>Select your preference and budget.</p>

    <select id="preference">
        <option value="all">Any Food</option>
        <option value="healthy">Healthy</option>
        <option value="spicy">Spicy</option>
        <option value="sweet">Sweet</option>
        <option value="snack">Snacks</option>
    </select>

    <input id="budget" type="number" min="1"
           value="100" placeholder="Budget in rupees">

    <br>
    <button onclick="recommendFood()">Recommend Food</button>
    <div id="recommendResult" class="result"></div>
</section>

<section id="cart">
    <h2>🛒 My Order</h2>
    <div id="cartItems">No items added.</div>
    <h3>Total: ₹<span id="total">0</span></h3>
    <button onclick="placeOrder()">Place Order</button>
    <button onclick="clearCart()">Clear Cart</button>
    <div id="billResult" class="result"></div>
</section>

<section id="admin">
    <h2>⚙️ Add Food Item</h2>
    <input id="newName" maxlength="60" placeholder="Food name">
    <input id="newPrice" type="number" min="1" placeholder="Price">

    <select id="newCategory">
        <option value="healthy">Healthy</option>
        <option value="spicy">Spicy</option>
        <option value="sweet">Sweet</option>
        <option value="snack">Snacks</option>
    </select>

    <br>
    <button onclick="addFood()">Add Food</button>
    <div id="adminResult" class="result"></div>
    <p>Demo admin feature without login.</p>
</section>

<footer>
    <p>FAI Mini Project | AI Cafeteria Management System</p>
</footer>

<script>
let foods = [];
let cart = [];

async function api(url, data = null) {
    const options = data === null ? {} : {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    };

    const response = await fetch(url, options);
    const result = await response.json();

    if (!response.ok) {
        throw new Error(result.error || "Request failed");
    }

    return result;
}

function escapeHTML(value) {
    return String(value).replace(/[&<>"']/g, c => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;"
    })[c]);
}

async function loadMenu() {
    try {
        foods = await api("/menu");
        displayMenu();
    } catch (error) {
        document.getElementById("foodMenu").textContent =
            "Could not load menu.";
    }
}

function displayMenu() {
    document.getElementById("foodMenu").innerHTML =
        foods.map(f => `
            <div class="card">
                <div class="emoji">${f.emoji}</div>
                <h3>${escapeHTML(f.name)}</h3>
                <p>Price: ₹${f.price}</p>
                <p>Category: ${f.category}</p>
                <button onclick="addToCart(${f.id})">
                    Add to Order
                </button>
            </div>
        `).join("");
}

function addToCart(id) {
    const food = foods.find(f => f.id === id);
    if (!food) return;

    const item = cart.find(i => i.id === id);

    if (item) {
        item.quantity++;
    } else {
        cart.push({id: id, quantity: 1});
    }

    displayCart();
}

function displayCart() {
    const div = document.getElementById("cartItems");

    if (!cart.length) {
        div.textContent = "No items added.";
    } else {
        div.innerHTML = cart.map(i => {
            const f = foods.find(x => x.id === i.id);
            return `<p>${escapeHTML(f.name)} × ${i.quantity}
                = ₹${f.price * i.quantity}
                <button onclick="removeItem(${i.id})">Remove</button>
                </p>`;
        }).join("");
    }

    let total = 0;

    cart.forEach(i => {
        const f = foods.find(x => x.id === i.id);
        total += f.price * i.quantity;
    });

    document.getElementById("total").textContent = total;
}

function removeItem(id) {
    cart = cart.filter(i => i.id !== id);
    displayCart();
}

function clearCart() {
    cart = [];
    displayCart();
    document.getElementById("billResult").textContent = "";
}

async function recommendFood() {
    const preference = document.getElementById("preference").value;
    const budget = Number(document.getElementById("budget").value);
    const div = document.getElementById("recommendResult");

    if (!Number.isFinite(budget) || budget <= 0) {
        div.textContent = "Please enter a valid budget.";
        return;
    }

    try {
        const result = await api("/recommend", {
            preference: preference,
            budget: budget
        });

        div.innerHTML = `<p>${escapeHTML(result.message)}</p>`;

        result.recommendations.forEach(f => {
            div.innerHTML += `
                <p>${f.emoji} ${escapeHTML(f.name)} — ₹${f.price}
                <button onclick="addToCart(${f.id})">Add</button></p>`;
        });
    } catch (error) {
        div.textContent = error.message;
    }
}

async function placeOrder() {
    const div = document.getElementById("billResult");

    if (!cart.length) {
        div.textContent = "Please add food to your order.";
        return;
    }

    try {
        const result = await api("/order", {items: cart});

        div.innerHTML = `
            <h3>${escapeHTML(result.message)}</h3>
            ${result.bill.map(i =>
                `<p>${escapeHTML(i.name)} × ${i.quantity}
                = ₹${i.amount}</p>`
            ).join("")}
            <h3>Final Bill: ₹${result.total}</h3>
        `;

        cart = [];
        displayCart();
    } catch (error) {
        div.textContent = error.message;
    }
}

async function addFood() {
    const name = document.getElementById("newName").value.trim();
    const price = Number(document.getElementById("newPrice").value);
    const category = document.getElementById("newCategory").value;
    const div = document.getElementById("adminResult");

    if (!name || !Number.isInteger(price) || price <= 0) {
        div.textContent = "Enter a valid name and positive price.";
        return;
    }

    try {
        const result = await api("/admin/add", {
            name: name,
            price: price,
            category: category
        });

        div.textContent = result.message;
        document.getElementById("newName").value = "";
        document.getElementById("newPrice").value = "";
        await loadMenu();
    } catch (error) {
        div.textContent = error.message;
    }
}

loadMenu();
displayCart();
</script>
</body>
</html>
"""


# ---------------- PYTHON ROUTES ----------------

@app.route("/")
def home():
    return render_template_string(HTML)


@app.route("/menu")
def get_menu():
    return jsonify(foods)


@app.route("/recommend", methods=["POST"])
def recommend_food():
    data = request.get_json(silent=True) or {}
    preference = data.get("preference", "all")

    if preference not in [
        "all", "healthy", "spicy", "sweet", "snack"
    ]:
        return jsonify({"error": "Invalid preference"}), 400

    try:
        budget = float(data.get("budget", 100))
        if budget <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid budget"}), 400

    # Rule-Based Artificial Intelligence
    recommendations = [
        f for f in foods
        if f["price"] <= budget
        and (preference == "all" or f["category"] == preference)
    ]

    message = (
        "Food recommended according to your preference and budget."
        if recommendations
        else "No matching food found. Try another budget or preference."
    )

    return jsonify({
        "message": message,
        "recommendations": recommendations
    })


@app.route("/order", methods=["POST"])
def place_order():
    data = request.get_json(silent=True) or {}
    items = data.get("items", [])

    if not isinstance(items, list) or not items:
        return jsonify({"error": "Cart is empty"}), 400

    bill = []
    total = 0

    for item in items:
        try:
            food_id = int(item["id"])
            quantity = int(item["quantity"])
        except (KeyError, ValueError, TypeError):
            return jsonify({"error": "Invalid order"}), 400

        food = next((f for f in foods if f["id"] == food_id), None)

        if food is None or not 1 <= quantity <= 100:
            return jsonify({"error": "Invalid item or quantity"}), 400

        amount = food["price"] * quantity
        total += amount

        bill.append({
            "name": food["name"],
            "quantity": quantity,
            "amount": amount
        })

    return jsonify({
        "message": "Order placed successfully!",
        "bill": bill,
        "total": total
    })


@app.route("/admin/add", methods=["POST"])
def add_food():
    data = request.get_json(silent=True) or {}

    name = str(data.get("name", "")).strip()
    category = data.get("category", "")

    try:
        price = int(data.get("price", 0))
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid price"}), 400

    if not name or len(name) > 60:
        return jsonify({"error": "Enter a valid food name"}), 400

    if price <= 0:
        return jsonify({"error": "Price must be positive"}), 400

    if category not in ["healthy", "spicy", "sweet", "snack"]:
        return jsonify({"error": "Invalid category"}), 400

    new_id = max((f["id"] for f in foods), default=0) + 1

    new_food = {
        "id": new_id,
        "name": name,
        "price": price,
        "category": category,
        "emoji": "🍽️"
    }

    foods.append(new_food)

    return jsonify({
        "message": "Food added successfully!",
        "food": new_food
    }), 201


# ---------------- RUN PROJECT ----------------

if __name__ == "__main__":
    app.run(debug=True)