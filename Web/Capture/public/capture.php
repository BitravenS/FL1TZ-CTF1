<?php

require __DIR__ . '/../vendor/autoload.php';

use Spatie\Browsershot\Browsershot;

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['url'])) {
    $url = $_POST['url'];

    if (!$url) {
        die("Invalid URL provided.");
    }
    $safe = filter_var($url,FILTER_VALIDATE_URL);
    if($safe){
    $screenshotDir = __DIR__ . "/screenshots/";
    }
    else{
        $screenshotDir = __DIR__ . "/forbidden/";
    }
    if (!file_exists($screenshotDir)) {
        mkdir($screenshotDir, 0777, true);
    }

    $imageName = md5($url) . '.png';
    $imagePath = $screenshotDir . $imageName;

    try {
        Browsershot::url($url)
            ->setOption('args', ['--no-sandbox', '--disable-gpu'])
            ->waitUntilNetworkIdle()
            ->save($imagePath);
        
        header("Location: ./index.php?image=" . $imageName);
    } catch (Exception $e) {
        die("Error capturing screenshot: " . $e->getMessage());
    }
} else {
    die("Invalid request.");
}
