# krew-info scraper

## Projected output

The krew.info service contains an HTML table matrix with cities (regional blood banks) and blood types (with destinction of their status). The scraper will produce the following output:

| Image value  | Blood banks indication |
| ------------ | ---------------------- | 
| `krew0.png`  | `STOP`                 |
| `krew11.png` | `ALMOST_FULL`          |
| `krew1.png`  | `OPTIMAL`              |
| `krew2.png`  | `MODERATE`             |
| `krew3.png`  | `CRITICAL`             |

```json
{
    "datetime_modified": "02.04.2023 12:30",
    "url_src": "https://krew.info/zapasy/",
    "blood_banks": { 
        "Białystok": {
            "0 Rh-": "FULL",
            "0 Rh+": "ALMOST_EMPTY"
        },
        "Gdańsk": {
            "0 Rh-": "FULL",
            "0 Rh+": "ALMOST_EMPTY"
        }
    },
}
```
