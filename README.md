# KZN Smart Mall Parking Management System

A command-line parking management application for three KwaZulu-Natal malls, supporting drivers, admins, and mall owners.

**Author:** Veliswa Boya | Student Number: 402601157 | BSc IT — 2026S1PR511AD

---

## Requirements

- Python 3.7+
- No external dependencies

---

## How to Run

```bash
python parking.py
```

---

## Supported Malls

| # | Mall | Location | Capacity | Pricing |
|---|------|----------|----------|---------|
| 1 | Gateway Theatre of Shopping | Umhlanga, Durban | 250 | Flat — R15.00 |
| 2 | Pavilion Shopping Centre | Westville, Durban | 180 | Hourly — R10.00/hr |
| 3 | La Lucia Mall | La Lucia, Durban | 150 | Capped — R12.00/hr (max R60.00) |

---

## User Roles

### Driver
- Select a mall
- Register car entry / exit
- View parking fee and make payment
- View current parking status, parking history, and payment history

### Admin
- Assigned to one mall at registration
- View currently parked cars
- Monitor parking capacity
- View daily parking activity

### Mall Owner / Stakeholder
- View details for all malls
- Generate cross-mall comparison reports (total cars, revenue, average duration)

---

## Data Files

| File | Description |
|------|-------------|
| `user.txt` | Registered users (`username\|password\|role\|mall_id`) |
| `parking.txt` | Parking records (`record_id\|username\|mall_id\|car_reg\|entry_time\|exit_time\|fee\|paid`) |
| `payments.txt` | Payment records (`payment_id\|record_id\|username\|mall_id\|amount\|payment_time`) |

These files are created automatically on first use.

---

## Pricing Logic

- **Flat** — Fixed fee regardless of duration (Gateway)
- **Hourly** — Fee = ⌈hours⌉ × rate (Pavilion)
- **Capped** — Hourly rate with a maximum daily cap (La Lucia)
# parking_system
This is a parking system that helps mall management keep close monitoring of parking spaces across a couple of malls that they own. I created this as part of a school project. I will redesign this as microservices at a later stage.
