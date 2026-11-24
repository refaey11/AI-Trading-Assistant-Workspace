# Master ZIP range preflight

This isolated audit branch performs read-only Dropbox byte-range inspection. The current preflight reads only the ZIP EOCD and central-directory metadata. It does not read local file headers or member payloads. The next gate is to identify the exact 2020 member from the central-directory listing before any member payload is requested. Data for 2025 and 2026 remains out of scope and must not be accessed.
