// Polyfill for crypto.randomUUID()
(function() {
    if (typeof crypto !== 'undefined' && !crypto.randomUUID) {
        console.log("Adding crypto.randomUUID polyfill");
        
        // Helper function to convert bytes to hexadecimal
        function bytesToHex(bytes) {
            return Array.from(bytes)
                .map(b => b.toString(16).padStart(2, '0'))
                .join('');
        }
        
        // Implement the randomUUID function using getRandomValues
        crypto.randomUUID = function() {
            // Generate 16 random bytes (128 bits)
            const bytes = new Uint8Array(16);
            crypto.getRandomValues(bytes);
            
            // Set the version (4) and variant bits according to RFC4122
            bytes[6] = (bytes[6] & 0x0f) | 0x40; // version 4 (random)
            bytes[8] = (bytes[8] & 0x3f) | 0x80; // variant 1 (RFC4122)
            
            // Format the UUID string
            return (
                bytesToHex(bytes.subarray(0, 4)) + '-' +
                bytesToHex(bytes.subarray(4, 6)) + '-' +
                bytesToHex(bytes.subarray(6, 8)) + '-' +
                bytesToHex(bytes.subarray(8, 10)) + '-' +
                bytesToHex(bytes.subarray(10, 16))
            );
        };
    }
})(); 