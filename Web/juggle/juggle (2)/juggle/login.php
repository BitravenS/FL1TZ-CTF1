<?php
session_start();

$valid_username = 'noucha';
$stored_password_hash = '0e83040045199349412529226650580242199033911168370379069085300385';

$error = '';
$success = '';
$flag='FL1TZ{Wh0_US3S_PHP_AnYWAy_???}';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'];
    $password = $_POST['password'];

    $provided_password_hash = hash('sha256', $password);

    if ($username == $valid_username && $provided_password_hash == $stored_password_hash) {
        $_SESSION['loggedin'] = true;
        $success = "Login successful! Welcome, $username. Here is your flag: $flag";
    } else {
        $error = "womp womp!";
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login Page</title>
    <link rel="stylesheet" href="style.css"> 
</head>
<body>
    <div class="login-container">
        <h1>Login</h1>

        <?php if ($error): ?>
            <div class="error"><?= htmlspecialchars($error) ?></div>
        <?php endif; ?>

        <?php if ($success): ?>
            <div class="success"><?= htmlspecialchars($success) ?></div>
        <?php endif; ?>

        <form method="POST" action="login.php">
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" name="username" id="username" required>
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" name="password" id="password" required>
            </div>
            <div class="form-group">
                <input type="submit" value="Login">
            </div>
        </form>
    </div>

    <div class="top-right-image">
        <img src="flitz.jpg" alt="Logo">
    </div>
</body>
</html>
