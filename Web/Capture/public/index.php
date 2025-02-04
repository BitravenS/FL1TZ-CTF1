<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Screenshot</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
    <div>
            <img src="./flitz.jpg" alt="Logo" class="top-right-image">
        </div>
        <h2>Capture Website Screenshot</h2>
        <form action="./capture.php" method="post">
            <input type="text" name="url" placeholder="Enter website URL..." required>
            <button type="submit">Capture Screenshot</button>
        </form>
        <?php if (isset($_GET['image'])): ?>
            <h3>Screenshot:</h3>
            <img src="/screenshots/<?php echo htmlspecialchars($_GET['image']); ?>" alt="Screenshot">
        <?php endif; ?>
    </div>
</body>
</html>
