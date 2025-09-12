<?php
exec('python3 gpey.py');

$jsonFile = 'data.json';
if (file_exists($jsonFile)) {
    $jsonData = file_get_contents($jsonFile);
    $data = json_decode($jsonData, true);

    if (json_last_error() === JSON_ERROR_NONE) {
        header('Content-Type: application/json');
        echo json_encode($data);
    } else {
        echo json_encode(['error' => 'Error decoding JSON data.']);
    }
} else {
    echo json_encode(['error' => 'JSON file not found.']);
}

?>