import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import random

# --- Page Configuration ---
st.set_page_config(
    page_title="Financial Aid 101: Your College Journey",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

BADGES = [
    {"name": "Aid Apprentice", "desc": "Completed your first learning module!", "icon": "🔰"},
    {"name": "FAFSA Filer", "desc": "Mastered the FAFSA concepts.", "icon": "📄"},
    {"name": "Aid Analyst", "desc": "Used the Net Price Calculator.", "icon": "🧮"},
    {"name": "Resource Explorer", "desc": "Visited the Resource Hub.", "icon": "🧭"},
    {"name": "Scholarship Seeker", "desc": "Learned about different aid types.", "icon": "💡"},
    {"name": "Knowledge Knight", "desc": "Completed all learning modules!", "icon": "🧠"},
    {"name": "Financial Aid Guru", "desc": "Earned all available badges!", "icon": "👑"},
]

# --- Custom CSS for a Friendly & Academic Look ---
st.markdown("""
<style>
    /* Main App Styling */
    .main {
        background-color: #F0F2F6; /* Light gray background */
        color: #333333; /* Dark gray text */
    }
    /* Sidebar Styling */
    .css-1d391kg {
        background-color: #FFFFFF;
    }
    /* Flashcard Styling */
    .flashcard {
        background-color: #FFFFFF;
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 20px;
        border: 1px solid #D0D0D0;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.05);
        transition: 0.3s;
    }
    .flashcard:hover {
        box-shadow: 0 8px 16px 0 rgba(0,0,0,0.1);
        border: 1px solid #0068C9; /* A friendly blue */
    }
    .flashcard h3 {
        color: #0068C9;
        font-size: 24px;
    }
    /* Info Box Styling for Definitions, Examples, Sources */
    .info-box {
        background-color: #f0f0f0 !important; /* Light gray */
        color: #222 !important;
        border-radius: 10px;
        padding: 18px 20px;
        margin-bottom: 12px;
        font-size: 16px;
        border: 1px solid #e0e0e0;
    }
    /* Button Styling */
    .stButton>button {
        border-radius: 20px;
        border: 1px solid #0068C9;
        background-color: #0068C9;
        color: white;
        padding: 10px 24px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #0052A0;
        color: white;
        border: 1px solid #0052A0;
    }
    /* Badge Styling */
    .badge {
        background-color: #E7F3FF; /* Light blue background */
        color: #0068C9;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 10px;
        border: 1px solid #B3D7FF;
    }
    .badge h4 {
        margin: 0;
        font-size: 18px;
        color: #0052A0;
    }
    .badge p {
        margin: 0;
        font-size: 14px;
        color: #333333;
    }
    /* NEW: Custom Success/Error boxes for quiz feedback */
    .quiz-feedback-correct {
        background-color: #E7F3FF; /* Light blue */
        color: #0052A0; /* Dark blue */
        border: 1px solid #B3D7FF;
        border-radius: 10px;
        padding: 15px;
        margin-top: 15px;
    }
    .quiz-feedback-incorrect {
        background-color: #FFD2D2; /* Light red */
        color: #D8000C; /* Dark red */
        border: 1px solid #FFBABA;
        border-radius: 10px;
        padding: 15px;
        margin-top: 15px;
    }
    /* NEW: Modern Quiz Option Styling */
    .quiz-option {
        background-color: #FFFFFF;
        border: 1px solid #D0D0D0;
        border-radius: 10px;
        padding: 12px 20px;
        margin: 8px 0;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 16px;
        color: #333333;
    }
    .quiz-option:hover {
        background-color: #E7F3FF;
        border-color: #0068C9;
        box-shadow: 0 2px 4px rgba(0,104,201,0.1);
    }
    .quiz-option.selected {
        background-color: #0068C9;
        color: white;
        border-color: #0068C9;
    }
</style>
""", unsafe_allow_html=True)


# --- EXPANDED FINANCIAL AID CONTENT with QUIZZES (Now with 5 levels per concept) ---
VOCAB = {
    "⭐ Getting Started": [
        {
            "term": "FAFSA (Free Application for Federal Student Aid)",
            "definition": "The official form students must fill out to apply for federal financial aid, including grants, work-study, and loans. It's the single most important application for aid. The FAFSA is also used by many states and colleges to determine eligibility for their own aid programs. It collects detailed information about your family's income, assets, and household size to calculate your Student Aid Index (SAI). The form is updated annually, and recent changes have simplified the process by allowing direct IRS data import. Filing early is crucial as some aid is limited and awarded on a first-come, first-served basis.",
            "example": "The FAFSA opens on October 1st each year. It's crucial to file it as early as possible, as some aid is first-come, first-served. You’ll need your Social Security Number, tax returns, and information about your family’s finances. For instance, a student from a low-income family might qualify for a full Pell Grant by filing early, while delays could mean missing out on state grants. Even high-income families should file, as it unlocks merit-based aid at many schools. Common mistakes include not reporting all assets or forgetting to sign the form electronically.",
            "quiz": [
                # Level 1: 2 options
                {"q": "What is the main purpose of the FAFSA?", "options": ["To apply for admission to college", "To apply for federal financial aid"], "correct": 1, "explanation": "The FAFSA is used exclusively to determine your eligibility for financial aid from the federal government, and many states and colleges also use it to award their own aid."},
                # Level 2: 4 options
                {"q": "If your parents are not U.S. citizens, can you still fill out the FAFSA?", "options": ["No, your parents must be citizens", "Yes, if you are a U.S. citizen or eligible noncitizen", "Yes, but you can only get loans", "No, you must apply for international aid"], "correct": 1, "explanation": "Your parents' citizenship status does not affect your eligibility for federal student aid. If you are a citizen or eligible noncitizen, you can and should file the FAFSA. Your parents can use a Taxpayer Identification Number (ITIN) or enter all zeros for their Social Security Number if they don't have one."},
                # Level 3: 6 options
                {"q": "Which of the following is NOT a type of aid you can get by filing the FAFSA?", "options": ["Pell Grant", "Federal Work-Study", "Private scholarships from local clubs", "Direct Subsidized Loans", "State grants", "Institutional aid from colleges"], "correct": 2, "explanation": "The FAFSA is for federal and often state/institutional aid. Private scholarships from organizations, companies, or clubs have their own separate application processes."},
                # Level 4: 7 options
                {"q": "What recent change has simplified the FAFSA process?", "options": ["It now requires a physical signature", "It allows direct IRS data import", "It is only available in paper form", "It no longer asks for family income", "It must be filed by mail", "It combines with college applications", "It automatically awards all aid"], "correct": 1, "explanation": "The FAFSA now integrates with IRS systems to pull tax data directly, reducing errors and time spent on manual entry."},
                # Level 5: 8 options
                {"q": "Why might a high-income family still benefit from filing the FAFSA?", "options": ["To access merit-based aid at many schools", "To qualify for private loans only", "To get tax refunds", "To apply for campus housing", "To secure athletic scholarships", "To unlock state-specific grants", "To receive work-study even without need", "To compare aid offers from multiple colleges"], "correct": 0, "explanation": "Even if not eligible for need-based aid, filing the FAFSA is often required for merit scholarships and allows families to compare comprehensive aid packages."}
            ]
        },
        {
            "term": "Cost of Attendance (COA)",
            "definition": "The total estimated cost to attend a college for one year. It includes tuition, fees, housing, food, books, supplies, transportation, and personal expenses. COA is used to determine your financial need and eligibility for aid. It varies by institution and can include both direct costs (billed by the school) and indirect costs (estimated living expenses). Public schools often have lower COA for in-state students, while private schools may have higher COA but more generous aid packages. Understanding COA helps in budgeting and comparing true college costs.",
            "example": "Don’t be scared by a college’s high COA! It’s the 'sticker price', and very few students pay the full amount. Financial aid is designed to lower this cost. For example, a college with a $60,000 COA may offer you $40,000 in grants and scholarships, resulting in a net price of $20,000. COA can fluctuate based on residency status, program type (e.g., engineering vs. liberal arts), and off-campus living choices. Always check the college's website for the most accurate COA breakdown, as it affects loan limits and aid calculations.",
            "quiz": [
                # Level 1: 2 options
                {"q": "Cost of Attendance (COA) is also known as the...", "options": ["Net Price", "Sticker Price"], "correct": 1, "explanation": "COA is the full, published cost before any grants or scholarships are applied. The 'Net Price' is the cost after that aid is deducted."},
                # Level 2: 4 options
                {"q": "Which of these is typically included in the Cost of Attendance?", "options": ["Tuition and fees only", "Tuition, housing, food, and books", "Only the amount you have to pay out-of-pocket", "The cost of a car to get to campus"], "correct": 1, "explanation": "COA is a comprehensive estimate that includes both direct costs (like tuition) and indirect costs (like books and personal expenses)."},
                # Level 3: 6 options
                {"q": "Why is it important to know a college's COA?", "options": ["It's the exact amount your family will have to pay", "It's used to calculate the amount of financial aid you are eligible for", "It determines your class schedule", "It's the amount you will owe in loans", "It sets your graduation date", "It affects your major choice"], "correct": 1, "explanation": "Financial aid offices calculate your 'financial need' by subtracting your Student Aid Index (SAI) from the COA. A higher COA can mean you are eligible for more aid."},
                # Level 4: 7 options
                {"q": "How does COA differ for in-state vs. out-of-state students at public universities?", "options": ["It's the same for everyone", "In-state is usually lower due to reduced tuition", "Out-of-state includes more fees", "In-state excludes housing costs", "Out-of-state adds travel expenses", "In-state is higher for residents", "It doesn't affect aid eligibility"], "correct": 1, "explanation": "Public schools subsidize tuition for in-state residents, leading to a lower COA compared to out-of-state students."},
                # Level 5: 8 options
                {"q": "What factor might cause a college's COA to be higher for certain programs?", "options": ["Liberal arts majors", "Engineering or lab-based programs with extra fees", "Online-only courses", "Part-time enrollment", "Summer sessions", "Athletic participation", "Study abroad options", "General education requirements"], "correct": 1, "explanation": "Programs requiring specialized equipment or labs often have additional fees built into the COA, increasing the total estimate."}
            ]
        },
        {
            "term": "Student Aid Index (SAI)",
            "definition": "An eligibility index number that a college’s financial aid office uses to determine how much federal student aid you would receive. It replaces the old Expected Family Contribution (EFC). The SAI is calculated from your FAFSA and can be as low as -1500. The formula considers income, assets, family size, and number of family members in college. Unlike EFC, SAI allows for negative values to better reflect high-need situations and doesn't divide contributions among multiple students. It's not the amount you pay but a tool for aid distribution.",
            "example": "The SAI is calculated using the information from your FAFSA. A lower SAI means you have a higher financial need and may be eligible for more aid. For example, if your SAI is -500 and the COA is $30,000, your financial need is $30,500. Families with multiple children in college benefit more under SAI, as it doesn't split the index. Errors in reporting untaxed income or assets can inflate your SAI, reducing aid. Always review your FAFSA Submission Summary for accuracy.",
            "quiz": [
                # Level 1: 2 options
                {"q": "A lower Student Aid Index (SAI) generally means you are eligible for...", "options": ["Less financial aid", "More financial aid"], "correct": 1, "explanation": "The SAI represents what the formula thinks your family can contribute. A lower number indicates greater financial need, which qualifies you for more need-based aid like Pell Grants."},
                # Level 2: 4 options
                {"q": "What information is used to calculate your SAI?", "options": ["Your high school grades", "Information from your FAFSA application", "A letter of recommendation", "Your intended college major"], "correct": 1, "explanation": "The SAI is calculated based on the financial information you and your family provide on the FAFSA, such as income, assets, and family size."},
                # Level 3: 6 options
                {"q": "Can your Student Aid Index be a negative number?", "options": ["No, the lowest it can be is 0", "Yes, it can go down to -1500", "Yes, but only for graduate students", "No, it is always equal to the tuition cost", "Yes, up to -5000", "No, it's always positive"], "correct": 1, "explanation": "A new feature of the SAI (compared to the old EFC) is that it can be as low as -1500, which helps colleges better identify students with the highest levels of financial need."},
                # Level 4: 7 options
                {"q": "How does SAI differ from the old EFC in handling multiple students in college?", "options": ["It splits the index among siblings", "It doesn't divide; each student gets their own full SAI", "It adds extra for each sibling", "It subtracts for each additional student", "It ignores siblings entirely", "It doubles for families with twins", "It remains unchanged from EFC"], "correct": 1, "explanation": "Unlike EFC, SAI calculates independently for each student without dividing, potentially increasing aid for families with multiple college attendees."},
                # Level 5: 8 options
                {"q": "What common error could artificially increase your SAI and reduce aid eligibility?", "options": ["Underreporting income", "Overreporting assets or untaxed income", "Forgetting to list all colleges", "Filing too early", "Using estimated taxes", "Not signing electronically", "Listing incorrect dependency status", "Omitting household size changes"], "correct": 1, "explanation": "Failing to accurately report assets or untaxed income sources like retirement contributions can inflate SAI, leading to less need-based aid."}
            ]
        },
        {
            "term": "Net Price",
            "definition": "The actual amount a student pays to attend a college in a single academic year after subtracting scholarships and grants from the total cost of attendance. It represents the 'out-of-pocket' cost and is a better indicator of affordability than COA. Net price calculators are required on college websites to provide personalized estimates. It can vary based on family income, assets, and merit factors. Understanding net price helps in comparing colleges beyond sticker prices and planning for long-term costs.",
            "example": "If a college’s COA is $50,000 and you receive $35,000 in grants and scholarships, your net price is $15,000. For a low-income student, net price at an elite private school might be lower than at a public university due to generous aid. Always use the college's official net price calculator for accurate estimates, as it factors in institutional aid policies. Net price doesn't include loans or work-study, which can further reduce costs but require repayment or work.",
            "quiz": [
                # Level 1: 2 options
                {"q": "How is Net Price different from Cost of Attendance?", "options": ["Net Price is the total cost before aid", "Net Price is the cost after grants and scholarships are subtracted"], "correct": 1, "explanation": "Net Price is what you actually pay after all gift aid is applied."},
                # Level 2: 4 options
                {"q": "What does Net Price represent?", "options": ["The full sticker price", "The out-of-pocket cost after gift aid", "Only tuition costs", "Loan amounts only"], "correct": 1, "explanation": "Net Price subtracts grants and scholarships from COA to show what you'll actually owe."},
                # Level 3: 6 options
                {"q": "Where can you find a tool to estimate your Net Price for a specific college?", "options": ["On the FAFSA website", "On each college's website (required by law)", "Only through private consultants", "In college brochures", "Via email request", "Not available until after admission"], "correct": 1, "explanation": "Colleges must provide net price calculators on their sites to help prospective students estimate costs based on their finances."},
                # Level 4: 7 options
                {"q": "Why might Net Price be lower at a private college than a public one for some students?", "options": ["Private colleges have lower COA", "Generous institutional aid packages", "Public colleges don't offer grants", "Private schools exclude fees", "Public aid is merit-only", "Private loans are cheaper", "Net price is always higher at privates"], "correct": 1, "explanation": "Many private colleges have large endowments allowing for substantial need-based and merit aid, reducing net price for qualified students."},
                # Level 5: 8 options
                {"q": "What factor is NOT typically included in Net Price calculations?", "options": ["Grants", "Scholarships", "Loans", "Tuition", "Housing costs", "Books and supplies", "Personal expenses", "Transportation"], "correct": 2, "explanation": "Net Price subtracts only gift aid (grants/scholarships); loans are borrowed money that must be repaid and aren't deducted."}
            ]
        },
        {
            "term": "CSS Profile",
            "definition": "An additional financial aid application required by many private colleges and universities to award their own institutional aid. It asks for more detailed financial information than the FAFSA, including home equity, medical expenses, and non-custodial parent info. Administered by the College Board, it's used by over 200 institutions. The CSS Profile has a fee but offers waivers for low-income families. It allows for explanations of special circumstances and is key for accessing non-federal aid at selective schools.",
            "example": "Some schools, especially selective private colleges, require the CSS Profile in addition to the FAFSA. The application opens on October 1st and has a fee, but fee waivers are available. For a divorced family, it might require info from both parents, potentially increasing aid if circumstances warrant. Completing it accurately can unlock thousands in institutional grants, but errors like not reporting business assets can delay processing.",
            "quiz": [
                # Level 1: 2 options
                {"q": "What is the CSS Profile used for?", "options": ["Federal aid only", "Institutional grants and scholarships"], "correct": 1, "explanation": "The CSS Profile is used by colleges to award their own funds, not federal or state aid."},
                # Level 2: 4 options
                {"q": "Which type of colleges most commonly require the CSS Profile?", "options": ["Public universities", "Private colleges and universities", "Community colleges", "Online-only schools"], "correct": 1, "explanation": "Selective private institutions use it to distribute their own aid more precisely."},
                # Level 3: 6 options
                {"q": "What additional information does CSS Profile ask for compared to FAFSA?", "options": ["Home equity", "Medical expenses", "Non-custodial parent finances", "High school grades", "Extracurricular activities", "Intended major"], "correct": 0, "explanation": "CSS Profile delves deeper into family finances, including assets like home equity not considered in FAFSA."},  # Note: Multiple could be correct, but picking one as per structure; adjust if needed
                # Level 4: 7 options
                {"q": "Who administers the CSS Profile?", "options": ["Federal government", "College Board", "Each individual college", "State education departments", "IRS", "FAFSA office", "Private banks"], "correct": 1, "explanation": "The College Board, known for SAT and AP, manages the CSS Profile."},
                # Level 5: 8 options
                {"q": "Under what circumstance might you get a fee waiver for CSS Profile?", "options": ["If you're a high school senior", "If your family income is low", "If you have good grades", "If you're applying to multiple colleges", "If you're an athlete", "If you filed FAFSA first", "If you're international", "If you request it in writing"], "correct": 1, "explanation": "Fee waivers are available for families meeting income criteria, similar to SAT waivers."}
            ]
        }
    ],
    "📄 The FAFSA Deep Dive": [
        {
            "term": "Federal Pell Grant",
            "definition": "A form of federal grant aid that is awarded to undergraduate students with exceptional financial need and does not have to be repaid. The maximum award changes each year and is determined by Congress. Eligibility is based on SAI, COA, and enrollment status. Pell Grants are portable across schools and can be used for up to 12 semesters. Recent expansions include eligibility for incarcerated students and those affected by school closures. The amount disbursed adjusts for part-time status, and lifetime limits apply.",
            "example": "The Pell Grant is the foundation of federal student aid. Your SAI is the primary factor in determining if you receive it and how much you get. For 2024-25, the maximum Pell Grant is $7,395. A full-time student with SAI of 0 might receive the max, while part-time reduces it proportionally. If you transfer schools, your Pell eligibility follows you. Overusing semesters could exhaust your lifetime limit before graduation.",
            "quiz": [
                # Level 1: 2 options
                {"q": "Do you have to repay a Federal Pell Grant?", "options": ["Yes, with interest", "No, it's free money for college"], "correct": 1, "explanation": "Grants are a form of gift aid, meaning they do not need to be repaid. This makes them the best type of financial aid."},
                # Level 2: 4 options
                {"q": "Who is eligible for a Pell Grant?", "options": ["All college students", "Undergraduate students with high financial need", "Only students with a 4.0 GPA", "Graduate students only"], "correct": 1, "explanation": "Pell Grants are specifically for undergraduate students who have not yet earned a bachelor's degree and who demonstrate significant financial need as determined by the FAFSA."},
                # Level 3: 6 options
                {"q": "What happens to your Pell Grant if you drop out or take fewer classes?", "options": ["Nothing, you keep all the money", "You might have to repay a portion of the grant", "It automatically converts into a loan", "You are banned from receiving aid in the future", "It increases for the next semester", "It transfers to another student"], "correct": 1, "explanation": "Your Pell Grant award is based on your enrollment status (full-time, half-time, etc.). If you change your enrollment, your award may be reduced, and in some cases, you may have to pay back the portion you were no longer eligible for."},
                # Level 4: 7 options
                {"q": "What is the lifetime limit for Pell Grant usage?", "options": ["6 semesters", "12 semesters (equivalent to 6 years full-time)", "Unlimited", "4 years only", "Depends on your major", "8 semesters for transfers", "No limit if GPA is high"], "correct": 1, "explanation": "Pell Grants can be used for up to 12 semesters or 600% of the scheduled award, encouraging timely graduation."},
                # Level 5: 8 options
                {"q": "Which recent change expanded Pell Grant eligibility?", "options": ["To graduate students", "To incarcerated individuals in certain programs", "To international students", "To high-income families", "To part-time workers only", "To online-only students", "To military veterans exclusively", "To students over 30"], "correct": 1, "explanation": "Recent legislation restored Pell eligibility for incarcerated students in approved prison education programs, promoting rehabilitation through education."}
            ]
        },
        {
            "term": "Federal Work-Study",
            "definition": "A program that provides part-time jobs for students with financial need, allowing them to earn money to help pay education expenses. Jobs may be on campus or with approved off-campus employers, often in community service roles. Earnings are paid directly to the student and don't count as income on future FAFSAs. The program emphasizes jobs related to your major or civic engagement. Awards are based on need and school funding, with hourly wages at least minimum wage. You can work up to 20 hours/week typically.",
            "example": "If you're awarded Work-Study, you get access to a special list of on-campus or community service jobs. The money you earn is paid directly to you, not to the school. You can use it for books, supplies, or personal expenses. For example, a biology major might work in a lab, gaining experience while earning. If you don't use your full award, it doesn't carry over, so plan accordingly.",
            "quiz": [
                # Level 1: 2 options
                {"q": "How do you receive money from a Federal Work-Study award?", "options": ["It's automatically applied to your tuition bill", "You receive a paycheck for the hours you work"], "correct": 1, "explanation": "Work-Study is not a grant. It's an opportunity to get a job and earn a paycheck, which you can then use for tuition, books, or personal expenses."},
                # Level 2: 4 options
                {"q": "Does accepting a Work-Study award guarantee you a job?", "options": ["Yes, the school must give you a job", "No, you still have to apply for and get a job", "Yes, but you can only work in the library", "No, it's just a loan"], "correct": 1, "explanation": "The award gives you the eligibility to apply for Work-Study positions. You are responsible for finding, applying for, and being hired for a specific job."},
                # Level 3: 6 options
                {"q": "What is a key benefit of a Work-Study job over a regular off-campus job?", "options": ["The pay is always much higher", "The earnings do not count against you on the next year's FAFSA", "You don't have to pay taxes on the earnings", "You get more vacation time", "It guarantees full-time hours", "It includes health benefits"], "correct": 1, "explanation": "This is a huge advantage! Money earned through Federal Work-Study is not counted as income on your subsequent FAFSA, which helps you remain eligible for more financial aid in the future."},
                # Level 4: 7 options
                {"q": "What types of jobs are prioritized in the Work-Study program?", "options": ["High-paying corporate internships", "Community service and major-related positions", "Off-campus retail jobs", "Full-time summer work", "Remote freelance gigs", "Athletic department roles only", "Library positions exclusively"], "correct": 1, "explanation": "Work-Study emphasizes jobs that benefit the community or align with your studies, enhancing your resume and experience."},
                # Level 5: 8 options
                {"q": "If you don't use your full Work-Study award in a year, what happens?", "options": ["It carries over to next year", "It is lost; awards are annual", "It converts to a grant", "It becomes a loan", "You get a refund", "It transfers to another student", "It increases your next award", "It affects your GPA"], "correct": 1, "explanation": "Work-Study funds are allocated per academic year and don't roll over, so maximize usage by securing a job early."}
            ]
        },
        {
            "term": "Verification",
            "definition": "A process where the college's financial aid office asks you to submit additional documents to confirm the information you reported on your FAFSA is accurate. About 18% of applicants are selected each year. Selection can be random or based on inconsistencies. Required documents often include tax transcripts, W-2s, or proof of non-filing. The process ensures aid integrity and can delay disbursement if not completed promptly. Some schools use IRS Data Retrieval Tool to streamline verification.",
            "example": "Don't panic if you're selected for verification! It's a common, random process. Just submit the requested documents (like tax forms) by the deadline. If you don’t, your aid can’t be disbursed. For instance, a student might need to provide a parent's tax transcript to confirm income. Delays can mean starting school without aid, so respond quickly.",
            "quiz": [
                # Level 1: 2 options
                {"q": "If you are selected for verification, it means...", "options": ["You did something wrong and are in trouble", "The school needs to confirm your FAFSA information"], "correct": 1, "explanation": "Verification is a routine quality-control process. It does not mean you are suspected of wrongdoing. It's crucial to respond promptly to any requests for documents."},
                # Level 2: 4 options
                {"q": "What is the most common document requested during verification?", "options": ["A high school transcript", "A personal essay", "Parent and student tax returns or transcripts", "A driver's license"], "correct": 2, "explanation": "Financial aid offices most often need to verify the income information reported on the FAFSA, so they will typically ask for copies of tax documents."},
                # Level 3: 6 options
                {"q": "What could happen if you don't complete the verification process?", "options": ["You will receive more financial aid", "You will not be able to receive any federal or institutional financial aid", "You will be automatically switched to a different major", "Nothing, it is an optional process", "Your FAFSA is deleted", "You get extra time to file"], "correct": 1, "explanation": "Completing verification is mandatory. If you fail to submit the required documents by the deadline, the financial aid office cannot disburse any funds to you, and you will be responsible for the full cost."},
                # Level 4: 7 options
                {"q": "How can some schools streamline the verification process?", "options": ["By skipping it entirely", "Using the IRS Data Retrieval Tool", "Requiring in-person meetings", "Charging a fee", "Only verifying high-income families", "Combining with admissions", "Automating via AI"], "correct": 1, "explanation": "The IRS DRT pulls tax data directly into FAFSA, often satisfying verification requirements without additional documents."},
                # Level 5: 8 options
                {"q": "What percentage of FAFSA applicants are typically selected for verification?", "options": ["5%", "About 18%", "50%", "100%", "Only 1%", "30%", "Varies by state", "Only first-time filers"], "correct": 1, "explanation": "Approximately 18% are selected annually, either randomly or due to data flags, to maintain program integrity."}
            ]
        },
        {
            "term": "Special Circumstances",
            "definition": "Situations that may affect your family’s ability to pay for college but are not reflected on the FAFSA, such as job loss, divorce, or high medical expenses. You can appeal for more aid by submitting documentation to your college’s financial aid office. This process, called professional judgment, allows aid administrators to adjust your SAI or aid package. Common circumstances include death in the family, natural disasters, or significant income reduction. Appeals must be made per school and aren't guaranteed.",
            "example": "If your parent loses their job after you file the FAFSA, you can request a 'professional judgment' review. The financial aid office may adjust your aid package based on your new circumstances. For example, documenting medical bills exceeding 10% of income could lead to increased grants. Always provide evidence like unemployment notices or hospital bills.",
            "quiz": [
                # Level 1: 2 options
                {"q": "What should you do if your family’s financial situation changes after you file the FAFSA?", "options": ["Nothing, you must wait until next year", "Contact your college’s financial aid office and request a review"], "correct": 1, "explanation": "Colleges can use 'professional judgment' to adjust your aid if you provide documentation of special circumstances."},
                # Level 2: 4 options
                {"q": "What is the process called when aid offices adjust for special circumstances?", "options": ["FAFSA amendment", "Professional judgment", "Aid recalculation", "Circumstance waiver"], "correct": 1, "explanation": "Professional judgment allows flexibility in aid awards based on documented changes."},
                # Level 3: 6 options
                {"q": "Which is an example of a special circumstance?", "options": ["Job loss", "Divorce", "High medical expenses", "Buying a new car", "Vacation costs", "Routine bills"], "correct": 0, "explanation": "Unexpected events like job loss that impact ability to pay can qualify for appeals."},
                # Level 4: 7 options
                {"q": "Do you need to appeal special circumstances at each college separately?", "options": ["No, one appeal covers all", "Yes, each school handles independently", "Only for private colleges", "FAFSA handles it automatically", "Only if aid is federal", "Appeals are not allowed", "Only for state aid"], "correct": 1, "explanation": "Each institution reviews appeals individually based on their policies and available funds."},
                # Level 5: 8 options
                {"q": "What documentation might be required for a special circumstances appeal?", "options": ["Unemployment notice", "Medical bills", "Divorce decree", "Death certificate", "Natural disaster proof", "Income reduction letters", "All of the above", "None, just a written statement"], "correct": 6, "explanation": "Comprehensive documentation is essential to substantiate the appeal and potentially increase aid."}
            ]
        },
        {
            "term": "Dependency Status",
            "definition": "Determines whether you are considered a dependent or independent student for federal aid purposes. Most students under 24 are considered dependent, but there are exceptions (married, military, orphan, etc.). Independent students don't report parental info, potentially increasing aid eligibility. Criteria include age, marital status, children, military service, homelessness, emancipation, or foster care. Status is determined by FAFSA questions and can affect SAI calculations significantly.",
            "example": "If you are 23, single, and not a veteran, you are likely a dependent student and must report your parents’ financial information on the FAFSA. However, if you're married or have a child, you're independent. A student who is an orphan or was in foster care since age 13 qualifies as independent, potentially accessing more aid without parental data.",
            "quiz": [
                # Level 1: 2 options
                {"q": "Which of the following makes you an independent student for FAFSA purposes?", "options": ["Being over 24", "Being married"], "correct": 0, "explanation": "There are several ways to qualify as independent, including age, marital status, military service, and more."},  # Note: Both are correct, but structure picks one
                # Level 2: 4 options
                {"q": "What is the primary age threshold for automatic independent status?", "options": ["18", "21", "24", "25"], "correct": 2, "explanation": "Students 24 or older are automatically independent and don't need parental financial info."},
                # Level 3: 6 options
                {"q": "Which situation does NOT qualify you as independent?", "options": ["Being married", "Having children you support", "Being in the military", "Living off-campus", "Being a ward of the court", "Being emancipated"], "correct": 3, "explanation": "Living arrangements alone don't determine dependency; specific criteria like marriage or military service do."},
                # Level 4: 7 options
                {"q": "How does independent status affect your FAFSA?", "options": ["You must include parental info", "You don't report parental finances", "It decreases aid eligibility", "It requires more documents", "It only applies to graduates", "It splits aid with siblings", "It guarantees Pell Grants"], "correct": 1, "explanation": "Independents base SAI on their own finances, often qualifying for more need-based aid."},
                # Level 5: 8 options
                {"q": "What is a less common way to qualify as independent?", "options": ["Being homeless or at risk", "Being in foster care since 13", "Being an emancipated minor", "Serving in the military", "Having legal guardianship", "Being a veteran", "All of the above", "Just turning 18"], "correct": 6, "explanation": "FAFSA recognizes various vulnerable situations for independent status to ensure aid access."}
            ]
        }
    ],
    "💸 Loans vs. Grants": [
        {
            "term": "Grant",
            "definition": "A form of financial aid that does not have to be repaid. Grants are often need-based and can come from the federal government, state governments, or colleges. They may have eligibility requirements like GPA maintenance or full-time enrollment. Federal grants like Pell are portable, while state grants often require residency. Institutional grants can be merit- or need-based. Grants reduce college costs directly and are prioritized in aid packages.",
            "example": "The Pell Grant is a federal grant. Many states and colleges also offer their own grants to students. For example, the Cal Grant in California or the Tuition Assistance Program (TAP) in New York. A student might receive a $5,000 institutional grant for high need, renewable with a 2.5 GPA.",
            "quiz": [
                # Level 1: 2 options
                {"q": "What is the main characteristic of a grant?", "options": ["It must be repaid with interest", "It does not need to be repaid"], "correct": 1, "explanation": "Grants are 'gift aid,' which is free money to help you pay for college. This is the best type of aid you can receive."},
                # Level 2: 4 options
                {"q": "Grants are usually awarded based on...", "options": ["Athletic ability", "Financial need", "Your intended major", "A random lottery"], "correct": 1, "explanation": "While some grants may have other criteria, the vast majority are 'need-based,' meaning they are awarded to students whose FAFSA shows they have difficulty paying for college."},
                # Level 3: 6 options
                {"q": "Which of these is a type of grant?", "options": ["Direct Unsubsidized Loan", "Federal Pell Grant", "Federal Work-Study", "Parent PLUS Loan", "State Cal Grant", "Institutional merit grant"], "correct": 1, "explanation": "The Pell Grant is a cornerstone of federal grant aid. The others are types of loans or work programs."},
                # Level 4: 7 options
                {"q": "What requirement might some grants have for renewal?", "options": ["Maintaining a minimum GPA", "Full-time enrollment", "Residency in the state", "Community service hours", "All of the above", "No requirements", "Only for federal grants"], "correct": 4, "explanation": "Many grants stipulate conditions like GPA or enrollment to continue receiving funds each year."},
                # Level 5: 8 options
                {"q": "How do state grants typically differ from federal ones?", "options": ["They require repayment", "They are often residency-based", "They are merit-only", "They exclude undergrads", "They are not need-based", "They can't be combined with Pell", "They are for graduates only", "They have no limits"], "correct": 1, "explanation": "State grants usually prioritize residents and may have unique eligibility tied to local policies."}
            ]
        },
        {
            "term": "Scholarship",
            "definition": "A form of financial aid that does not have to be repaid. Scholarships are typically merit-based, awarded for academic achievement, talent, or other specific criteria. Some scholarships are need-based or have a combination of requirements. They can be one-time or renewable, from various sources like colleges, corporations, or nonprofits. Scholarships may require essays, interviews, or portfolios, and some are highly competitive with national scopes.",
            "example": "You can find scholarships from colleges, companies, and non-profits for everything from good grades to community service to being left-handed! Some scholarships are for specific majors, backgrounds, or interests. The National Merit Scholarship is awarded to students with top PSAT scores. The Gates Scholarship supports high-achieving, low-income minority students.",
            "quiz": [
                # Level 1: 2 options
                {"q": "Scholarships are most often awarded based on...", "options": ["Financial need", "Merit, talent, or specific criteria"], "correct": 1, "explanation": "While some scholarships consider need, most are 'merit-based,' meaning you earn them through your achievements, skills, or background."},
                # Level 2: 4 options
                {"q": "Do you have to repay scholarships?", "options": ["Yes, after you graduate", "No, they are a form of gift aid", "Only if your grades drop", "Yes, but they are interest-free"], "correct": 1, "explanation": "Like grants, scholarships are free money that you do not have to pay back."},
                # Level 3: 6 options
                {"q": "Where is the best place to look for scholarships?", "options": ["Only on the FAFSA website", "Only from the federal government", "From many sources, including colleges, non-profits, and online search engines", "You don't need to look; they are awarded automatically", "Only local libraries", "Exclusively through high schools"], "correct": 2, "explanation": "Scholarship hunting requires effort! You should check with the financial aid offices of the colleges you're applying to, use free online search engines, and check with local community organizations."},
                # Level 4: 7 options
                {"q": "What makes a scholarship 'competitive'?", "options": ["High award amounts", "National scope and many applicants", "Requirement for essays or interviews", "Specific criteria like major or background", "All of the above", "Only local availability", "No application needed"], "correct": 4, "explanation": "Competitive scholarships often have rigorous applications and select few winners from large pools."},
                # Level 5: 8 options
                {"q": "Which is an example of a unique scholarship criterion?", "options": ["Being left-handed", "Duck calling talent", "Prom dress made of duct tape", "Zombie apocalypse essay", "Tall students", "Vegetarian advocacy", "All of the above", "Standard GPA only"], "correct": 6, "explanation": "Many scholarships have quirky or specific criteria to stand out and attract niche applicants."}
            ]
        },
        {
            "term": "Direct Subsidized Loan",
            "definition": "A federal student loan for undergraduates with financial need. The U.S. Department of Education pays the interest while you're in school at least half-time, during the grace period, and during deferment periods. Borrowing limits apply based on year in school, with lower rates than private loans. Repayment begins after grace period, with options like income-driven plans. These loans build credit and offer forgiveness programs for public service.",
            "example": "If you qualify, this is the best type of loan to take. You won't accrue any interest until after you graduate, saving you a lot of money. For a freshman, the limit is $3,500, increasing yearly.",
            "quiz": [
                # Level 1: 2 options
                {"q": "What is the key benefit of a Subsidized Loan?", "options": ["The loan does not need to be repaid", "The government pays the interest while you are in school"], "correct": 1, "explanation": "The interest 'subsidy' from the government is the main advantage. This means the loan balance won't grow while you are focused on your studies."},
                # Level 2: 4 options
                {"q": "Who is eligible for a Direct Subsidized Loan?", "options": ["All students", "Undergraduate students with demonstrated financial need", "Parents of students", "Graduate students"], "correct": 1, "explanation": "Subsidized loans are strictly need-based and are only available to undergraduate students."},
                # Level 3: 6 options
                {"q": "When does interest start to accrue on a Subsidized Loan?", "options": ["The day you take out the loan", "After you graduate or drop below half-time enrollment", "It never accrues interest", "After you get your first job", "During summer breaks", "Only if you transfer schools"], "correct": 1, "explanation": "Interest begins to accrue after the 'grace period,' which is typically six months after you leave school. Until then, the government covers it."},
                # Level 4: 7 options
                {"q": "What is the annual borrowing limit for a freshman with a Subsidized Loan?", "options": ["$2,500", "$3,500", "$4,500", "$5,500", "$6,500", "Unlimited", "Depends on COA"], "correct": 1, "explanation": "Limits start at $3,500 for first-year undergrads and increase to $5,500 for juniors/seniors."},
                # Level 5: 8 options
                {"q": "Which repayment option is available for Subsidized Loans?", "options": ["Standard 10-year plan", "Income-driven repayment", "Public Service Loan Forgiveness", "Extended repayment", "Graduated repayment", "Deferment for hardship", "All of the above", "None, must pay immediately"], "correct": 6, "explanation": "Federal loans offer flexible repayment and forgiveness options, making them superior to private loans."}
            ]
        },
        {
            "term": "Direct Unsubsidized Loan",
            "definition": "A federal student loan available to undergraduate and graduate students; there is no requirement to demonstrate financial need. Interest begins to accrue from the moment the loan is disbursed. You can pay interest while in school to avoid capitalization. Limits are higher than subsidized, and rates are fixed. These loans offer similar protections as subsidized, including deferment and forbearance.",
            "example": "Interest begins to accrue on this loan from the moment it's disbursed. You can pay the interest while in school to prevent it from being added to your principal. For undergrads, limits are $5,500-$12,500 per year.",
            "quiz": [
                # Level 1: 2 options
                {"q": "What is the main difference between a Subsidized and an Unsubsidized loan?", "options": ["There is no difference", "Who is responsible for paying interest while you are in school"], "correct": 1, "explanation": "With an Unsubsidized loan, you (the borrower) are responsible for all interest that accrues, starting from day one. With a Subsidized loan, the government covers that interest for you."},
                # Level 2: 4 options
                {"q": "Is eligibility for an Unsubsidized Loan based on financial need?", "options": ["Yes, it is strictly need-based", "No, financial need is not a requirement"], "correct": 1, "explanation": "Any eligible student can receive an Unsubsidized Loan, regardless of their family's income or SAI."},
                # Level 3: 6 options
                {"q": "What happens if you don't pay the interest on your Unsubsidized Loan while in school?", "options": ["The interest is forgiven", "The interest gets capitalized (added to your loan balance)", "The loan is cancelled", "Your interest rate goes down", "It converts to subsidized", "You get a grace period extension"], "correct": 1, "explanation": "Capitalization means the interest that accrued is added to the principal amount of your loan. You then start paying interest on the new, larger balance, which costs you more money over time."},
                # Level 4: 7 options
                {"q": "What is the maximum annual limit for Unsubsidized Loans for independent undergrads?", "options": ["$5,500", "$7,500", "$9,500", "$12,500", "$20,500 for grads", "No limit", "Same as subsidized"], "correct": 3, "explanation": "Independent students can borrow up to $12,500 per year in Unsubsidized Loans, higher than dependent limits."},
                # Level 5: 8 options
                {"q": "How can you avoid interest capitalization on Unsubsidized Loans?", "options": ["Ignore it until graduation", "Pay the interest while in school", "Request deferment annually", "Convert to subsidized", "Use work-study earnings", "Apply for forgiveness early", "All except ignore", "Capitalization is unavoidable"], "correct": 1, "explanation": "Making interest payments during school prevents it from adding to the principal, saving money long-term."}
            ]
        },
        {
            "term": "Parent PLUS Loan",
            "definition": "A federal loan that parents of dependent undergraduate students can use to help pay for college. The parent, not the student, is responsible for repaying this loan. It requires a credit check, has higher interest rates, and no borrowing limits beyond COA minus other aid. Repayment begins immediately, but deferment is available. PLUS loans offer some federal protections but less flexibility than student loans.",
            "example": "If your family needs to borrow more than the federal student loan limits, your parent can apply for a Parent PLUS Loan. These loans require a credit check and have higher interest rates than student loans. For example, a parent might borrow $10,000 at 7% interest.",
            "quiz": [
                # Level 1: 2 options
                {"q": "Who is responsible for repaying a Parent PLUS Loan?", "options": ["The student", "The parent who took out the loan"], "correct": 1, "explanation": "The parent is legally responsible for repaying the loan, not the student."},
                # Level 2: 4 options
                {"q": "What is required to qualify for a Parent PLUS Loan?", "options": ["Financial need demonstration", "A credit check", "Student's high GPA", "Parent's employment history"], "correct": 1, "explanation": "Unlike student loans, PLUS requires checking the parent's credit for adverse history."},
                # Level 3: 6 options
                {"q": "When does repayment typically begin for Parent PLUS Loans?", "options": ["After student graduates", "Immediately after disbursement", "During student's grace period", "Only if student defaults", "After deferment request", "Never if income is low"], "correct": 1, "explanation": "Repayment starts right away, though parents can request deferment while the student is in school."},
                # Level 4: 7 options
                {"q": "What is the borrowing limit for Parent PLUS Loans?", "options": ["$5,500 per year", "COA minus other aid", "$10,000 maximum", "Same as student limits", "No limit", "Based on parent's income", "Only for tuition"], "correct": 1, "explanation": "Parents can borrow up to the full COA after other aid, making it a gap-filler."},
                # Level 5: 8 options
                {"q": "Why might a parent be denied a PLUS Loan?", "options": ["Adverse credit history", "Student's low grades", "High family income", "Not filing FAFSA", "Student is independent", "Parent is retired", "Loan for grad student", "All except grades"], "correct": 0, "explanation": "Denials are based on credit issues like bankruptcies or defaults, not income or student factors."}
            ]
        },
        {
            "term": "Private Student Loan",
            "definition": "A loan from a bank, credit union, or private lender to help pay for college. Private loans usually have higher interest rates and fewer protections than federal loans. They often require a co-signer, have variable rates, and limited repayment options. Eligibility based on credit score, not need. Use as a last resort after exhausting federal options, and compare terms carefully.",
            "example": "You should only consider private loans after exhausting all federal aid options. Compare interest rates, repayment terms, and borrower protections before borrowing. For instance, a private loan might have a 10% variable rate vs. federal's 5% fixed.",
            "quiz": [
                # Level 1: 2 options
                {"q": "What is a major risk of private student loans?", "options": ["They have lower interest rates", "They may require a co-signer and have fewer repayment options"], "correct": 1, "explanation": "Private loans often require a co-signer and do not offer income-driven repayment or loan forgiveness options."},
                # Level 2: 4 options
                {"q": "When should you consider private loans?", "options": ["As a first option", "After exhausting federal aid", "Only for grad school", "Never"], "correct": 1, "explanation": "Federal loans have better terms and protections, so max them out first."},
                # Level 3: 6 options
                {"q": "What do private loans typically lack compared to federal?", "options": ["Fixed interest rates", "Income-driven repayment", "Loan forgiveness programs", "Deferment options", "Credit checks", "Co-signer requirements"], "correct": 1, "explanation": "Private loans don't offer federal benefits like IDR or PSLF."},
                # Level 4: 7 options
                {"q": "What factor determines private loan eligibility?", "options": ["FAFSA SAI", "Credit score", "High school GPA", "Intended major", "State residency", "All of the above", "None, automatic approval"], "correct": 1, "explanation": "Lenders assess creditworthiness, often requiring a co-signer for students with limited history."},
                # Level 5: 8 options
                {"q": "Why are private loan rates often variable?", "options": ["Tied to market indexes", "Change with borrower's income", "Fixed by federal law", "Lower than federal", "Only for short terms", "Guaranteed not to increase", "Based on college ranking", "All variable by default"], "correct": 0, "explanation": "Variable rates fluctuate with economic conditions, potentially increasing costs over time."}
            ]
        }
    ],
    "🎓 Scholarships 101": [
        {
            "term": "Scholarship",
            "definition": "A form of financial aid that does not have to be repaid. Scholarships are awarded for academic achievement, athletic talent, artistic ability, leadership, community service, unique backgrounds, or other criteria. Some are need-based, but most are merit-based. They can range from small local awards to full-ride national prizes. Renewable scholarships require meeting ongoing criteria, while one-time ones are disbursed once.",
            "example": "The National Merit Scholarship is awarded to students with top PSAT scores. The Gates Scholarship supports high-achieving, low-income minority students. There are also scholarships for first-generation students, women in STEM, and even for being left-handed!",
            "quiz": [
                # Level 1: 2 options
                {"q": "What is the main difference between a scholarship and a grant?", "options": ["Scholarships are always merit-based, grants are always need-based", "Scholarships are usually merit-based, grants are usually need-based"], "correct": 1, "explanation": "Most scholarships are awarded for achievements or special criteria, while grants are typically based on financial need."},
                # Level 2: 4 options
                {"q": "Do you have to pay back a scholarship?", "options": ["Yes, after graduation", "No, unless you violate the terms (like dropping out or failing to meet GPA requirements)"], "correct": 1, "explanation": "Scholarships are gift aid, but you may lose them if you don’t meet the requirements."},
                # Level 3: 6 options
                {"q": "Which of the following is NOT a common type of scholarship?", "options": ["Merit-based", "Need-based", "Random lottery", "Athletic", "Community service", "Identity-based"], "correct": 2, "explanation": "While some scholarships are awarded by lottery, most are based on merit, need, or specific criteria."},
                # Level 4: 7 options
                {"q": "What might be required in a scholarship application?", "options": ["Essay", "Transcripts", "Letters of recommendation", "Interview", "Portfolio", "All of the above", "Just a name"], "correct": 5, "explanation": "Applications often include multiple components to assess qualifications."},
                # Level 5: 8 options
                {"q": "How can scholarships be 'stacked'?", "options": ["Combining multiple awards", "Only if from same source", "Not allowed at all", "Only for merit ones", "Requires college approval", "Automatically deducted from loans", "Limited to $1,000 total", "Only renewable ones"], "correct": 0, "explanation": "Stacking means using several scholarships together, but check college policies as some limit total aid."}
            ]
        },
        {
            "term": "Types of Scholarships",
            "definition": "Scholarships come in many forms: merit-based (for grades, test scores, or talent), need-based, athletic, community service, identity-based (for certain backgrounds), major-specific, and more. Some are one-time awards, others are renewable. National vs. local, full-ride vs. partial, and employer-sponsored are other categories.",
            "example": "A college may offer a $10,000 renewable merit scholarship for students with a 3.8 GPA. A local Rotary Club may offer a $500 community service scholarship. Some scholarships are for specific majors, like engineering or nursing.",
            "quiz": [
                # Level 1: 2 options
                {"q": "What is a merit-based scholarship awarded for?", "options": ["Financial need", "Achievements like grades or talent"], "correct": 1, "explanation": "Merit scholarships reward excellence in academics, arts, or other areas."},
                # Level 2: 4 options
                {"q": "Athletic scholarships are typically offered by?", "options": ["NCAA Division I and II schools", "All colleges", "Only community colleges", "Non-profits"], "correct": 0, "explanation": "Division I and II provide athletic aid, while DIII focuses on academics."},
                # Level 3: 6 options
                {"q": "What is an identity-based scholarship?", "options": ["For specific ethnicities or backgrounds", "For first-generation students", "For LGBTQ+ individuals", "For women in STEM", "All of the above", "Only for athletes"], "correct": 4, "explanation": "These target underrepresented groups to promote diversity."},
                # Level 4: 7 options
                {"q": "What distinguishes a full-ride scholarship?", "options": ["Covers tuition only", "Covers all COA including room and board", "One-time payment", "For part-time students", "Renewable annually", "National competition", "Local only"], "correct": 1, "explanation": "Full-ride covers comprehensive costs, rare and highly competitive."},
                # Level 5: 8 options
                {"q": "Employer-sponsored scholarships are often for?", "options": ["Employees' children", "Specific industries", "Company loyalty", "Tuition reimbursement", "All of the above", "Only executives", "Short-term courses", "International travel"], "correct": 4, "explanation": "Companies offer these to support workforce development and family benefits."}
            ]
        },
        {
            "term": "How to Find Scholarships",
            "definition": "You can find scholarships from colleges, high schools, local organizations, employers, religious groups, and online search engines. Start early and apply to as many as you qualify for. Use free tools, avoid paid services, and check eligibility carefully. Networking and counselor advice can uncover hidden opportunities.",
            "example": "Use free search engines like Fastweb, College Board, or Scholarships.com. Check with your school counselor, local businesses, and community groups. Many scholarships have deadlines in the fall or winter of your senior year.",
            "quiz": [
                # Level 1: 2 options
                {"q": "Where should you look for scholarships?", "options": ["Only on the FAFSA website", "From many sources, including online search engines and local organizations"], "correct": 1, "explanation": "Cast a wide net! Many scholarships go unclaimed each year because students don’t apply."},
                # Level 2: 4 options
                {"q": "When should you start searching for scholarships?", "options": ["After college acceptance", "As early as possible, even junior year", "Only senior year", "After graduation"], "correct": 1, "explanation": "Early searching allows time to meet deadlines and gather materials."},
                # Level 3: 6 options
                {"q": "What is a free scholarship search engine?", "options": ["Fastweb", "Scholarships.com", "College Board BigFuture", "All of the above", "Paid consultants", "FAFSA only"], "correct": 3, "explanation": "These platforms match you with opportunities without fees."},
                # Level 4: 7 options
                {"q": "Why avoid paid scholarship services?", "options": ["They guarantee awards", "They are often scams", "They charge high fees for free info", "They reduce competition", "They are illegal", "They only find small awards", "All except guarantees"], "correct": 1, "explanation": "Legitimate scholarships don't require payment to apply or search."},
                # Level 5: 8 options
                {"q": "How can networking help find scholarships?", "options": ["Through community leaders", "Employer connections", "Alumni associations", "Religious groups", "All of the above", "Only online", "Not helpful", "Only for athletes"], "correct": 4, "explanation": "Personal connections can reveal unadvertised or local opportunities."}
            ]
        },
        {
            "term": "How to Apply for Scholarships",
            "definition": "Each scholarship has its own application process. Most require an application form, an essay or personal statement, transcripts, and sometimes letters of recommendation. Some require interviews or portfolios. Tailor materials to each, meet deadlines, and proofread thoroughly.",
            "example": "A typical application might ask for a 500-word essay about your goals, a copy of your transcript, and a letter from a teacher. Always follow instructions and proofread your materials.",
            "quiz": [
                # Level 1: 2 options
                {"q": "What is a common requirement for scholarship applications?", "options": ["A personal essay", "A video game score"], "correct": 0, "explanation": "Most scholarships require an essay or personal statement."},
                # Level 2: 4 options
                {"q": "Why tailor your essay to each scholarship?", "options": ["To show genuine interest", "To match their criteria", "To increase chances", "All of the above"], "correct": 3, "explanation": "Customizing demonstrates effort and alignment with the award's goals."},
                # Level 3: 6 options
                {"q": "What should you do before submitting?", "options": ["Proofread multiple times", "Get feedback", "Check all requirements", "Meet the deadline", "All of the above", "Submit early drafts"], "correct": 4, "explanation": "Thorough review ensures a polished, complete application."},
                # Level 4: 7 options
                {"q": "For art scholarships, what might be required?", "options": ["Portfolio of work", "Performance video", "Artist statement", "All of the above", "Just grades", "Essay only", "Interview"], "correct": 3, "explanation": "Creative scholarships often need evidence of talent beyond academics."},
                # Level 5: 8 options
                {"q": "What is a tip for recommendation letters?", "options": ["Choose recommenders who know you well", "Provide them context", "Give ample time", "Follow up politely", "All of the above", "Random teachers", "Write it yourself", "Not necessary"], "correct": 4, "explanation": "Strong, personalized letters can significantly boost your application."}
            ]
        },
        {
            "term": "Renewable vs. One-Time Scholarships",
            "definition": "Some scholarships are one-time awards, while others are renewable for multiple years if you meet certain requirements (like maintaining a GPA). Renewable ones provide ongoing support, but you must reapply or submit proof annually.",
            "example": "A $2,000 scholarship that renews for four years is worth $8,000 total. Make sure you understand the renewal criteria.",
            "quiz": [
                # Level 1: 2 options
                {"q": "What must you do to keep a renewable scholarship?", "options": ["Nothing, it renews automatically", "Meet the scholarship’s requirements, like GPA or enrollment status"], "correct": 1, "explanation": "Read the fine print! You may need to submit grades or proof of enrollment each year."},
                # Level 2: 4 options
                {"q": "What is a benefit of renewable scholarships?", "options": ["One-time payment", "Ongoing funding for multiple years", "Easier to apply", "No requirements"], "correct": 1, "explanation": "They provide stable support throughout college if criteria are met."},
                # Level 3: 6 options
                {"q": "Common renewal requirement?", "options": ["Minimum GPA", "Full-time enrollment", "Progress reports", "All of the above", "Changing majors", "Part-time work"], "correct": 3, "explanation": "Sponsors ensure continued eligibility through academic performance."},
                # Level 4: 7 options
                {"q": "What happens if you fail to meet renewal criteria?", "options": ["Automatic extension", "Loss of future funding", "Conversion to loan", "Appeal possible", "All except automatic", "No consequences", "Full refund required"], "correct": 1, "explanation": "You may lose the scholarship, but some allow appeals or probation."},
                # Level 5: 8 options
                {"q": "How do one-time scholarships differ?", "options": ["Disbursed once", "No renewal process", "Often smaller amounts", "Easier to win", "All of the above", "Always larger", "Require annual apps", "Guaranteed renewal"], "correct": 4, "explanation": "One-time awards provide a single boost without ongoing obligations."}
            ]
        },
        {
            "term": "Stacking Scholarships",
            "definition": "Some colleges allow you to combine ('stack') multiple scholarships, while others limit the total amount you can receive. Always check your college’s policy. Stacking can reduce out-of-pocket costs but may affect need-based aid.",
            "example": "If you win a $5,000 outside scholarship and a $10,000 college scholarship, your school may reduce your institutional aid. Ask the financial aid office how outside scholarships affect your package.",
            "quiz": [
                # Level 1: 2 options
                {"q": "What should you do if you win an outside scholarship?", "options": ["Do nothing", "Notify your college’s financial aid office"], "correct": 1, "explanation": "Colleges are required to coordinate all aid, so you must report outside scholarships."},
                # Level 2: 4 options
                {"q": "Why might a college reduce aid when you stack scholarships?", "options": ["To prevent over-awarding", "Policy on total gift aid", "To encourage loans", "All of the above"], "correct": 0, "explanation": "Schools ensure aid doesn't exceed COA, adjusting packages accordingly."},
                # Level 3: 6 options
                {"q": "What is 'over-awarding' in stacking?", "options": ["Receiving more aid than COA", "Can lead to aid reduction", "May require refunds", "All of the above", "Encouraged by colleges", "Only for merit aid"], "correct": 3, "explanation": "Federal rules prohibit aid exceeding costs, so stacking is monitored."},
                # Level 4: 7 options
                {"q": "Which colleges are more likely to allow full stacking?", "options": ["Public universities", "Private colleges with large endowments", "Community colleges", "For-profit schools", "All allow it", "None allow it", "Depends on policy"], "correct": 6, "explanation": "Policies vary; some replace need-based aid, others add on top."},
                # Level 5: 8 options
                {"q": "How can stacking affect need-based aid?", "options": ["May reduce grants", "Outside awards count as resources", "Can lower SAI", "Triggers verification", "All except lower SAI", "Increases loans", "No impact", "Always beneficial"], "correct": 0, "explanation": "Outside scholarships can offset need-based aid, but some schools minimize reductions."}
            ]
        },
        {
            "term": "Scholarship Scams",
            "definition": "Legitimate scholarships never charge a fee to apply. Beware of scams that ask for money, promise guaranteed awards, or request sensitive personal information. Report suspicious offers to authorities.",
            "example": "If a website asks you to pay to apply for a scholarship, it’s a scam. Use trusted sources and never pay for scholarship searches.",
            "quiz": [
                # Level 1: 2 options
                {"q": "What is a red flag for a scholarship scam?", "options": ["A fee to apply", "A requirement for an essay"], "correct": 0, "explanation": "Never pay to apply for a scholarship."},
                # Level 2: 4 options
                {"q": "What should you do with scam offers?", "options": ["Pay the fee", "Report to FTC or authorities", "Ignore them", "Share with friends"], "correct": 1, "explanation": "Reporting helps protect others from fraud."},
                # Level 3: 6 options
                {"q": "Common scam tactic?", "options": ["Guaranteed win promises", "Requests for bank info", "Unsolicited emails", "All of the above", "Free applications", "Essay requirements"], "correct": 3, "explanation": "Scams prey on desperation with false guarantees and info theft."},
                # Level 4: 7 options
                {"q": "Where to verify legitimate scholarships?", "options": ["BBB or FTC websites", "College financial aid offices", "Trusted search engines", "All of the above", "Social media ads", "Unknown emails", "Paid services"], "correct": 3, "explanation": "Cross-check with reliable sources to avoid fraud."},
                # Level 5: 8 options
                {"q": "Why do scams target scholarship seekers?", "options": ["High desperation for funds", "Easy to promise guarantees", "Collect personal data", "Charge hidden fees", "All of the above", "To help students", "Provide real awards", "Government backed"], "correct": 4, "explanation": "Scammers exploit vulnerability for financial gain or identity theft."}
            ]
        }
    ]
}

# Data for other pages (needed for the app to run)
AID_FACTS = [
    {"fact": "Over 85% of full-time undergraduate students receive some form of financial aid. You are not alone in needing help to pay for college!", "source": "NCES"},
    {"fact": "Filing the FAFSA is completely free. If a website asks you to pay to file the FAFSA, it's a scam. Always use the official studentaid.gov site.", "source": "Federal Student Aid"},
    {"fact": "Many colleges use the CSS Profile application in addition to the FAFSA to award their own institutional grants and scholarships. Check if your colleges require it!", "source": "College Board"},
    {"fact": "You have to fill out the FAFSA every year you are in college to remain eligible for federal and state aid.", "source": "Federal Student Aid"},
    {"fact": "Students who complete the FAFSA are far more likely to enroll in and complete college. It's one of the most important steps in your journey!", "source": "NCES"},
]

AID_TYPES = [
    {"name": "Grants", "type": "Gift Aid (Free Money)", "repayment": "No", "description": "Grants are typically awarded based on financial need. They are the best form of aid because they do not need to be repaid. The Federal Pell Grant is a common example."},
    {"name": "Scholarships", "type": "Gift Aid (Free Money)", "repayment": "No", "description": "Scholarships are usually awarded based on merit, such as academic achievement, athletic talent, or community service. You can find them from colleges, companies, and non-profits."},
    {"name": "Federal Work-Study", "type": "Self-Help Aid", "repayment": "Earned, not repaid", "description": "A need-based program that provides part-time jobs for students. You earn a paycheck to help cover expenses. Money earned here isn't counted against you on next year's FAFSA."},
    {"name": "Federal Student Loans", "type": "Self-Help Aid", "repayment": "Yes, with interest", "description": "Borrowed money that you must repay with interest. Federal loans have better benefits and lower fixed interest rates than private loans. Subsidized loans are best, as the government pays the interest while you're in school."},
]


# --- Session State Initialization ---
def init_session_state():
    if 'current_module' not in st.session_state:
        st.session_state.current_module = list(VOCAB.keys())[0]
    if 'card_indices' not in st.session_state:
        st.session_state.card_indices = {module: 0 for module in VOCAB.keys()}
    if 'module_progress' not in st.session_state:
        st.session_state.module_progress = {module: 0 for module in VOCAB.keys()}
    if 'badges' not in st.session_state:
        st.session_state.badges = set()
    if 'calculator_uses' not in st.session_state:
        st.session_state.calculator_uses = 0
    if 'resources_visited' not in st.session_state:
        st.session_state.resources_visited = False
    if 'aid_types_visited' not in st.session_state:
        st.session_state.aid_types_visited = False
    if 'active_quiz' not in st.session_state:
        st.session_state.active_quiz = None

init_session_state()

# --- Helper Functions ---
def check_and_award_badges():
    """Checks progress and awards badges."""
    if any(v > 0 for v in st.session_state.module_progress.values()):
        st.session_state.badges.add("Aid Apprentice")
    if st.session_state.module_progress.get("📄 The FAFSA Deep Dive", 0) >= len(VOCAB["📄 The FAFSA Deep Dive"]):
        st.session_state.badges.add("FAFSA Filer")
    if st.session_state.calculator_uses > 0:
        st.session_state.badges.add("Aid Analyst")
    if st.session_state.resources_visited:
        st.session_state.badges.add("Resource Explorer")
    if st.session_state.aid_types_visited:
        st.session_state.badges.add("Scholarship Seeker")
  
    all_modules_completed = all(st.session_state.module_progress[m] >= len(VOCAB[m]) for m in VOCAB)
    if all_modules_completed:
        st.session_state.badges.add("Knowledge Knight")
  
    if len(st.session_state.badges) >= len(BADGES) - 1:
        st.session_state.badges.add("Financial Aid Guru")

# --- UI Pages ---

def page_home():
    st.title("🎓 Welcome to Financial Aid 101")
    st.markdown("Your friendly guide to navigating financial aid for college. We're here to help you understand the process, from the FAFSA to your aid offer.")
  
    st.subheader("Your Progress")
    cols = st.columns(2)
    total_cards = sum(len(v) for v in VOCAB.values())
    completed_cards = sum(st.session_state.module_progress.values())
    progress = completed_cards / total_cards if total_cards > 0 else 0
  
    cols[0].metric("Learning Progress", f"{completed_cards}/{total_cards} Concepts", f"{progress:.0%} Mastered")
    cols[1].metric("Badges Earned", f"{len(st.session_state.badges)}/{len(BADGES)}", "Keep learning!")
    st.progress(progress)
  
    st.subheader("🏅 Recently Earned Badges")
    if not st.session_state.badges:
        st.info("Start learning in the 'Learning Modules' to earn your first badge!")
    else:
        badges_to_show = [b for b in BADGES if b['name'] in st.session_state.badges]
        num_columns = min(len(badges_to_show), 4)
        cols = st.columns(num_columns or 1)
        for i, badge in enumerate(badges_to_show):
            with cols[i % num_columns]:
                st.markdown(f"""
                <div class="badge">
                    <h4>{badge['icon']} {badge['name']}</h4>
                    <p>{badge['desc']}</p>
                </div>
                """, unsafe_allow_html=True)

# --- MODIFIED FUNCTION: display_quiz with modern option styling ---
def display_quiz(card, module_name, card_index, module_vocab):
    """Handles the display and logic of a single quiz question with a modern UI and pop-ups."""
    quiz_info = st.session_state.active_quiz
    level = quiz_info['level']
  
    if level > len(card.get('quiz', [])):
        st.success("🏆 You've mastered this topic! No more questions.")
        st.session_state.active_quiz = None
        st.rerun()
        return

    quiz_data = card['quiz'][level - 1]
  
    # Use a container for a modern, boxed look
    with st.container(border=True):
        st.subheader(f"📝 Test Your Knowledge: Level {level}")
      
        st.markdown(f"**{quiz_data['q']}**")
      
        # Modern sleek options using custom HTML/CSS instead of boring radio
        options = quiz_data['options']
        correct_index = quiz_data['correct']
      
        # Display options as clickable divs
        selected = None
        for i, opt in enumerate(options):
            key = f"option_{module_name}_{card_index}_{level}_{i}"
            if st.button(opt, key=key, help="Click to select"):
                selected = i
      
        if selected is not None:
            if selected == correct_index:
                # NEW: Pop-up "toast" notification for correct answer
                st.toast("Congrats! That's the right answer!", icon="🎉")
                
                # NEW: Custom styled feedback box instead of st.success
                st.markdown(f"""
                <div class="quiz-feedback-correct">
                    <strong>Correct!</strong> {quiz_data['explanation']}
                </div>
                """, unsafe_allow_html=True)
                
                st.session_state.active_quiz['status'] = 'passed'
            else:
                # NEW: Pop-up "toast" notification for incorrect answer
                st.toast("Not quite... Review the explanation and try again.", icon="🤔")

                # NEW: Custom styled feedback box instead of st.error/st.info
                st.markdown(f"""
                <div class="quiz-feedback-incorrect">
                    <strong>Not quite.</strong> The correct answer was: <strong>'{options[correct_index]}'</strong>.
                    <hr style="border-top: 1px solid #D8000C; margin: 8px 0; opacity: 0.5;">
                    <strong>Why?</strong> {quiz_data['explanation']}
                </div>
                """, unsafe_allow_html=True)
                
                st.session_state.active_quiz['status'] = 'failed'
            st.rerun()

    quiz_status = st.session_state.active_quiz.get('status')
    quiz_level = st.session_state.active_quiz['level']

    if quiz_status == 'passed':
        if quiz_level == 1 and st.session_state.module_progress[module_name] == card_index:
            st.session_state.module_progress[module_name] += 1
            check_and_award_badges()

        cols = st.columns(2)
        with cols[1]:
            if st.button("Continue to Next Concept →", key="continue_next"):
                st.session_state.card_indices[module_name] = min(card_index + 1, len(module_vocab) - 1)
                st.session_state.active_quiz = None
                st.rerun()
        with cols[0]:
            if quiz_level < 5:  # Updated to 5 levels
                if st.button(f"Try Level {quiz_level + 1} Question", key="try_harder"):
                    st.session_state.active_quiz['level'] += 1
                    st.session_state.active_quiz['status'] = 'pending'
                    st.rerun()
    elif quiz_status == 'failed':
        if st.button("Try Again", key="try_again"):
            st.session_state.active_quiz['status'] = 'pending'
            st.rerun()

def page_learning_modules():
    st.title("📚 Learning Modules")
    st.sidebar.title("Modules")
  
    current_selection = st.sidebar.radio("Select a learning module:", list(VOCAB.keys()), key="module_selector")
    if st.session_state.current_module != current_selection:
        st.session_state.current_module = current_selection
        st.session_state.active_quiz = None 
        st.rerun()

    module_name = st.session_state.current_module
    module_vocab = VOCAB[module_name]
    card_index = st.session_state.card_indices.get(module_name, 0)
    card = module_vocab[card_index]

    if st.session_state.active_quiz and st.session_state.active_quiz['card_index'] == card_index:
        display_quiz(card, module_name, card_index, module_vocab)
    else:
        st.header(f"{module_name} ({card_index + 1}/{len(module_vocab)})")
        st.markdown(f"""
        <div class="flashcard">
            <h3>{card['term']}</h3>
            <div class="info-box"><strong>Definition:</strong> {card['definition']}</div>
            <div class="info-box"><strong>💡 Pro Tip:</strong> <em>{card['example']}</em></div>
        </div>
        """, unsafe_allow_html=True)

        if card_index >= st.session_state.module_progress.get(module_name, 0):
            if st.button("Test My Understanding", key=f"test_{card_index}"):
                st.session_state.active_quiz = {'module': module_name, 'card_index': card_index, 'level': 1, 'status': 'pending'}
                st.rerun()
        else:
            st.success("✅ You've mastered this topic. Feel free to review or move on.")

        st.markdown("---")
        cols = st.columns(2)
        with cols[0]:
            if card_index > 0:
                if st.button("← Previous"):
                    st.session_state.card_indices[module_name] -= 1
                    st.session_state.active_quiz = None
                    st.rerun()
        with cols[1]:
            if card_index < st.session_state.module_progress.get(module_name, 0) and card_index < len(module_vocab) - 1:
                if st.button("Next →"):
                    st.session_state.card_indices[module_name] += 1
                    st.session_state.active_quiz = None
                    st.rerun()

def page_net_price_calculator():
    st.title("🧮 Net Price & Loan Calculator")
    st.markdown("Estimate what you might actually pay for college and how much you might need to borrow. This is an estimate for one academic year.")
  
    fact = random.choice(AID_FACTS)
    st.info(f"💡 **Did You Know?** {fact['fact']}")

    with st.form(key='net_price_form'):
        st.subheader("Enter Your College's Costs & Aid")
        cols = st.columns(2)
        coa = cols[0].number_input("College's Total Cost of Attendance (COA)", min_value=0, value=35000, step=1000, help="Find this on the college's financial aid website. It includes tuition, fees, housing, etc.")
        sai = cols[1].number_input("Your Student Aid Index (SAI / EFC)", min_value=-1500, value=5000, step=100, help="This comes from your FAFSA Submission Summary.")
      
        grants = st.number_input("Total Grants (Pell Grant, state grants, college grants)", min_value=0, value=10000, step=500, help="Add up all grant aid you were offered. This is free money.")
        scholarships = st.number_input("Total Scholarships", min_value=0, value=2000, step=500, help="Add up all scholarships from the college or outside sources. This is also free money.")
      
        submit_button = st.form_submit_button(label='Calculate Net Price')

    if submit_button:
        st.session_state.calculator_uses += 1
        check_and_award_badges()

        st.header("Your Estimated Financial Picture")
      
        gift_aid = grants + scholarships
        net_price = coa - gift_aid
        remaining_need = net_price - sai
      
        st.markdown(f"**Total Cost of Attendance (COA):** `${coa:,.2f}`")
        st.markdown(f"**Total Gift Aid (Grants & Scholarships):** `- ${gift_aid:,.2f}`")
        st.markdown("---")
        st.subheader(f"Your Estimated Net Price is: `${net_price:,.2f}`")
        st.caption("This is your estimated cost for one year after free money is applied.")
      
        cols = st.columns(2)
        cols[0].metric("Your Student Aid Index (SAI)", f"${sai:,.2f}", help="This is what the FAFSA formula suggests your family can contribute.")
        cols[1].metric("Remaining Gap / Potential Loans", f"${remaining_need:,.2f}", help="This is the amount you may need to cover with work-study, savings, or student loans.")

        if remaining_need > 0:
            st.warning(f"You have a remaining gap of **${remaining_need:,.2f}**. This might be covered by Federal Work-Study or Federal Student Loans. Let's estimate a loan payment for this amount.")
          
            # Simple loan estimation
            loan_amount = remaining_need
            interest_rate = 0.055 # Average federal student loan rate
            loan_term_years = 10
          
            monthly_rate = interest_rate / 12
            num_payments = loan_term_years * 12
            monthly_payment = (loan_amount * monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)
          
            st.subheader("Sample Loan Repayment Estimate")
            st.markdown(f"If you borrowed **${loan_amount:,.2f}** for *one year*, your estimated monthly payment for that single loan over 10 years would be:")
            st.metric("Estimated Monthly Payment", f"${monthly_payment:,.2f}/month")
            st.caption("Note: This is a simplified estimate for one year of borrowing. The total amount you borrow over 4+ years will be higher.")

def page_types_of_aid():
    st.title("💡 Types of Financial Aid")
    st.markdown("Understanding the difference between grants, scholarships, loans, and work-study is key. Prioritize 'Gift Aid' whenever possible!")
    st.session_state.aid_types_visited = True
    check_and_award_badges()

    for aid_type in AID_TYPES:
        with st.container():
            st.markdown(f"### {aid_type['name']}")
            repayment_text = "Needs to be Repaid" if aid_type['repayment'] == "Yes, with interest" else "Does NOT Need to be Repaid"
            repayment_color = "red" if aid_type['repayment'] == "Yes, with interest" else "green"
            st.markdown(f"**Type:** `{aid_type['type']}` | **Repayment:** :{repayment_color}[{repayment_text}]")
            st.markdown(f"""<div class="info-box">{aid_type['description']}</div>""", unsafe_allow_html=True)
            st.markdown("---")

def page_resource_hub():
    st.title("🧭 Resource Hub")
    st.markdown("Here are some official and trusted resources to help you on your financial aid journey.")
    st.session_state.resources_visited = True
    check_and_award_badges()

    st.subheader("Official Government & Application Sites")
    st.markdown("""<div class="info-box">- <b><a href="https://studentaid.gov/" target="_blank">StudentAid.gov</a></b>: The official federal government site. File your FAFSA here, manage loans, and find official information.</div>""", unsafe_allow_html=True)
    st.markdown("""<div class="info-box">- <b><a href="https://cssprofile.collegeboard.org/" target="_blank">CSS Profile</a></b>: An online application used by many private colleges to award their own institutional aid. Check if your colleges require it.</div>""", unsafe_allow_html=True)
  
    st.subheader("Free Scholarship Search Engines")
    st.markdown("""<div class="info-box">- <b><a href="https://www.fastweb.com/" target="_blank">Fastweb</a></b>: One of the largest and most popular free scholarship search websites.</div>""", unsafe_allow_html=True)
    st.markdown("""<div class="info-box">- <b><a href="https://www.scholarships.com/" target="_blank">Scholarships.com</a></b>: Another major, free platform for finding scholarship opportunities.</div>""", unsafe_allow_html=True)
    st.markdown("""<div class="info-box">- <b><a href="https://scholarships.collegeboard.org/" target="_blank">College Board's Scholarship Search</a></b>: A trusted search tool from the creators of the SAT and AP tests.</div>""", unsafe_allow_html=True)

    st.subheader("Tools for First-Generation & Immigrant Students")
    st.markdown("""<div class="info-box">- <b><a href="https://immigrantsrising.org/" target="_blank">Immigrants Rising</a></b>: Provides resources and scholarships for undocumented students.</div>""", unsafe_allow_html=True)
    st.markdown("""<div class="info-box">- <b><a href="https://www.thedream.us/" target="_blank">TheDream.US</a></b>: A major scholarship provider for DREAMers.</div>""", unsafe_allow_html=True)
    st.markdown("""<div class="info-box">- <b><a href="https://www.bestcolleges.com/resources/first-generation-students/" target="_blank">First-Generation Student Resources</a></b>: A guide with tips and resources specifically for first-gen students.</div>""", unsafe_allow_html=True)

# --- Main App Logic & Sidebar Navigation ---

st.sidebar.title("Financial Aid 101")
st.sidebar.markdown("---")

page = st.sidebar.radio("Navigation", [
    "🏠 Home",
    "📚 Learning Modules",
    "🧮 Net Price Calculator",
    "💡 Types of Aid",
    "🧭 Resource Hub",
])

st.sidebar.markdown("---")
st.sidebar.info("This is an educational tool. All calculations are estimates. Always consult official financial aid offers and websites.")

# Routing
if page == "🏠 Home":
    page_home()
elif page == "📚 Learning Modules":
    page_learning_modules()
elif page == "🧮 Net Price Calculator":
    page_net_price_calculator()
elif page == "💡 Types of Aid":
    page_types_of_aid()
elif page == "🧭 Resource Hub":
    page_resource_hub()