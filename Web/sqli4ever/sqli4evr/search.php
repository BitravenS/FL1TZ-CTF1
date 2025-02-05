<?php
session_start();

if (!isset($_SESSION['user'])) {
    header("Location: index.php");
    exit;
}

$host = getenv('DB_HOST') ;
$dbname = getenv('DB_NAME');
$username = getenv('DB_USER');
$password = getenv('DB_PASS');

try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname", $username, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
  //  echo "Connected successfully!";
} catch (PDOException $e) {
    // echo "Connection failed: ";
}
$books = [];
if ($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['book_id'])) {
    $book_id = $_GET['book_id'];

    $query = "SELECT id, title, author FROM books WHERE id = '$book_id'";
    try {
        $stmt = $pdo->query($query);
        $books = $stmt->fetchAll(PDO::FETCH_ASSOC);
    } catch (PDOException $e) {
        echo "Error: " ;
    }
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Search Books</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <img src="flitz.jpg" alt="User Image">
    </header>
    <h1>Search Books</h1>
    <p>Welcome, <?php echo htmlspecialchars($_SESSION['user']['name']); ?>!</p>

    <form method="GET">
        <input type="text" name="book_id" placeholder="Enter Book ID" required>
        <button type="submit">Search</button>
    </form>

    <?php if (!empty($books)): ?>
        <h2>Search Results</h2>
        <ul>
            <?php foreach ($books as $book): ?>
                <li><?php echo "ID: " . htmlspecialchars($book['id']) . ", Title: " . htmlspecialchars($book['title']) . ", Author: " . htmlspecialchars($book['author']); ?></li>
            <?php endforeach; ?>
        </ul>
    <?php endif; ?>

    <?php
    if ($_SESSION['user']['name'] === 'victor') {
        echo "<h2>Congratulations! Here is your flag: FL1TZ{3XCEl_1S_B3TT3R_anyWay}</h2>";
    }
    ?>
</body>
</html>
