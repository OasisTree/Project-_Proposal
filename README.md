# IsQueueNek: Centralized Scholarship Management System

IsQueueNek is a modular, Python-based desktop application with a Tkinter GUI designed to streamline the discovery, application, and management of scholarships. It serves as a centralized platform where student applicants and verified scholarship providers can interact efficiently, eliminating the need for scattered sources, repetitive submissions, and manual processing.

Through the use of a Master Student Profile, the system allows students to input their information once and automatically matches them with scholarships they qualify for based on predefined criteria like Grade Weighted Average (GWA), annual family income, and location.

---

## The Problem & Our Solution

Traditional scholarship systems in the Philippines are often fragmented, inefficient, and prone to misinformation. Students are forced to search across multiple platforms, verify legitimacy manually, submit repetitive physical documents, and endure long queues.

IsQueueNek resolves these major issues by providing a centralized, secure, and automated digital platform:

* **Combating Scams & Misinformation:** Only authorized organizations can post scholarships. Provider accounts are subject to an Admin approval gate (pending, approved, or rejected statuses) before they can access the dashboard.
* **Eliminating Physical Queuing:** The system replaces in-person document submission with a fully digital application process, including local file attachments for proof of income and grades.
* **Reducing Redundant Data Entry:** The Master Student Profile enables data reuse. Students store their academic and financial data once and apply to multiple eligible scholarships with a single click.

---

## Key Features

### For Students
* **Master Student Profile:** Store personal, academic, and financial data once.
* **Document Uploads:** Attach local files (PDFs, Images) for CTC of Grades and Proof of Income directly to your profile.
* **Automated Eligibility Screening:** The system filters out unqualified programs instantly based on GWA, income, and location.
* **One-Click Application:** Apply to eligible scholarships digitally.
* **Application Tracking:** Monitor status (pending, approved, rejected) in real-time.

### For Scholarship Providers
* **Verified Provider Dashboard:** A secure workspace accessible only after Admin approval.
* **Custom Scholarship Posting:** Define specific requirements (deadline, minimum GWA, maximum income limit, location, and total slots).
* **Automated Slot Management:** System tracks available slots and automatically deducts them upon application.
* **Applicant Assessment:** View a filtered list of pending applicants, review their profiles, and easily approve or reject them.

---

## System Architecture & Technologies

IsQueueNek is built using Python with a strong focus on modularity and security:

* **Frontend:** Tkinter for a clean, card-based Graphical User Interface.
* **Data Persistence:** JSON-based file handling (simulating a NoSQL database) managed through dedicated load_db and save_db utilities.
* **Security:** Implements password hashing and verification to protect user credentials.
* **Data Flow:** Uses Python dictionaries, lists, and class-based object-oriented programming to handle structured data, filtering algorithms, and UI state management.

---

## How It Works

1. **Onboarding:** User selects a role (Student or Provider) and registers. Provider accounts enter a pending state until Admin verification.
2. **Authentication:** Users log in securely via hashed credentials.
3. **Dashboard Navigation:** * Providers post new scholarships with specific eligibility criteria.
   * Students view a dynamically generated list of scholarships that explicitly match their Master Profile stats.
4. **Processing:** Students apply with one click. The system logs the application and updates the provider's slot count.
5. **Assessment:** Providers review applicant data and update the status (Approve or Reject), which is instantly reflected on the student's dashboard.

---

## Future Roadmap

* **Web Migration:** Transition from a local desktop application to a full web-based platform.
* **Relational Database:** Integration with a robust backend database (e.g., MySQL or PostgreSQL).
* **Email Notifications:** Automated email alerts for application status updates and impending deadlines.
* **Advanced Recommender:** A more complex recommendation algorithm based on degree programs and specific skill sets.
