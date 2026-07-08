"use client";

import { useState, useRef, useEffect } from "react";
import { FileText, Send, Briefcase, FileSearch, HelpCircle, Map, Upload, FileSignature } from "lucide-react";
import { motion } from "framer-motion";

export default function Home() {
  const [activeTab, setActiveTab] = useState("upwork");
  const [resumeText, setResumeText] = useState("");
  const [jdText, setJdText] = useState("");
  
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);

  // Upwork states
  const [hiringRate, setHiringRate] = useState("80%+");
  const [paymentVerified, setPaymentVerified] = useState(true);
  const [proposal, setProposal] = useState("");

  // Other features states
  const [atsResult, setAtsResult] = useState<any>(null);
  const [coverLetter, setCoverLetter] = useState("");
  const [questions, setQuestions] = useState("");
  const [roadmap, setRoadmap] = useState("");
  const [tailoredResume, setTailoredResume] = useState("");
  const [bookmarkletHref, setBookmarkletHref] = useState("");

  useEffect(() => {
    if (typeof window !== "undefined") {
      const origin = window.location.origin;
      const code = `javascript:(function(){
        const jd = document.querySelector('.fe-proposal-job-description, .job-description, [data-qa="job-description"], .cfe-ui-job-details-content')?.innerText || document.body.innerText;
        let hireRate = "Unknown";
        document.querySelectorAll('li, div').forEach(el => {
          if(el.innerText.toLowerCase().includes('hire rate')) {
            const match = el.innerText.match(/\\d+%/);
            if(match) hireRate = match[0];
          }
        });
        const paymentVerified = document.body.innerText.toLowerCase().includes('payment verified') ? 'true' : 'false';
        const url = '${origin}/?jd=' + encodeURIComponent(jd) + '&rate=' + encodeURIComponent(hireRate) + '&payment=' + paymentVerified;
        window.open(url, '_blank');
      })();`;
      setBookmarkletHref(code);
      
      const params = new URLSearchParams(window.location.search);
      const jd = params.get("jd");
      const rate = params.get("rate");
      const payment = params.get("payment");
      if (jd) setJdText(decodeURIComponent(jd));
      if (rate) setHiringRate(decodeURIComponent(rate));
      if (payment) setPaymentVerified(payment === "true");
    }
  }, []);

  const fileInputRef = useRef<HTMLInputElement>(null);

  const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch(`${API_BASE}/api/upload_resume`, {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setResumeText(data.text);
    } catch (error) {
      alert("Error uploading file.");
    }
    setUploading(false);
  };

  const handleGenerateProposal = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/upwork_proposal`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ resume_text: resumeText, jd_text: jdText, hiring_rate: hiringRate, payment_verified: paymentVerified, other_notes: "" })
      });
      const data = await res.json();
      setProposal(data.proposal);
    } catch (e) { alert("Error generating proposal."); }
    setLoading(false);
  };

  const handleAtsAnalysis = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/ats_analysis`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ resume_text: resumeText, jd_text: jdText })
      });
      const data = await res.json();
      setAtsResult(data.result);
    } catch (e) { alert("Error analyzing ATS."); }
    setLoading(false);
  };

  const handleCoverLetter = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/cover_letter`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ resume_text: resumeText, jd_text: jdText })
      });
      const data = await res.json();
      setCoverLetter(data.cover_letter);
    } catch (e) { alert("Error generating cover letter."); }
    setLoading(false);
  };

  const handleInterview = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/interview_questions`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ resume_text: resumeText, jd_text: jdText })
      });
      const data = await res.json();
      setQuestions(data.questions);
    } catch (e) { alert("Error generating questions."); }
    setLoading(false);
  };

  const handleRoadmap = async () => {
    if (!atsResult || !atsResult.missing_skills) {
      alert("Please run ATS Analysis first to find missing skills.");
      return;
    }
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/roadmap`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ missing_skills: atsResult.missing_skills })
      });
      const data = await res.json();
      setRoadmap(data.roadmap);
    } catch (e) { alert("Error generating roadmap."); }
    setLoading(false);
  };

  const handleTailorResume = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/tailor_resume`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ resume_text: resumeText, jd_text: jdText })
      });
      const data = await res.json();
      setTailoredResume(data.html);
    } catch (e) { alert("Error tailoring resume."); }
    setLoading(false);
  };

  const handleDownloadPDF = () => {
    if (!tailoredResume) return;
    // We trigger the native print dialog on the current window.
    // We will add print CSS to hide everything except the resume preview.
    window.print();
  };

  const tabs = [
    { id: "upwork", label: "Upwork Proposal", icon: Briefcase },
    { id: "tailor", label: "Tailor Resume", icon: FileSignature },
    { id: "ats", label: "ATS Analysis", icon: FileSearch },
    { id: "cover", label: "Cover Letter", icon: FileText },
    { id: "interview", label: "Interview", icon: HelpCircle },
    { id: "roadmap", label: "Roadmap", icon: Map },
  ];

  return (
    <div className="flex h-screen overflow-hidden">
      {/* Sidebar */}
      <div className="w-64 bg-gray-900 border-r border-gray-800 p-6 flex flex-col gap-6">
        <div className="flex items-center gap-3 text-xl font-bold text-blue-400">
          <div className="w-8 h-8 rounded-lg bg-blue-500/20 flex items-center justify-center">🤖</div>
          Copilot
        </div>

        <nav className="flex flex-col gap-2 mt-4">
          {tabs.map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 ${
                activeTab === tab.id ? "bg-blue-600 text-white shadow-lg shadow-blue-900/50" : "text-gray-400 hover:bg-gray-800 hover:text-gray-200"
              }`}
            >
              <tab.icon size={20} />
              <span className="font-medium">{tab.label}</span>
            </button>
          ))}
        </nav>
      </div>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto p-8 relative">
        <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-blue-600/10 rounded-full blur-[120px] pointer-events-none" />
        
        <div className="max-w-4xl mx-auto relative z-10 space-y-8">
          <header>
            <h1 className="text-4xl font-extrabold tracking-tight">AI Career Suite</h1>
            <p className="text-gray-400 mt-2 text-lg">Secure jobs faster with intelligent proposals and deep analysis.</p>
          </header>

          <div className="grid grid-cols-2 gap-6">
            <div className="space-y-2 relative">
              <div className="flex justify-between items-center">
                <label className="text-sm font-semibold text-gray-300">Resume Content</label>
                <input type="file" accept=".pdf" className="hidden" ref={fileInputRef} onChange={handleFileUpload} />
                <button 
                  onClick={() => fileInputRef.current?.click()}
                  className="text-xs bg-gray-800 hover:bg-gray-700 text-gray-300 px-3 py-1 rounded-lg flex items-center gap-2 transition"
                >
                  <Upload size={14} /> {uploading ? "Extracting..." : "Upload PDF"}
                </button>
              </div>
              <textarea 
                className="w-full h-32 bg-gray-900/50 border border-gray-700 rounded-2xl p-4 focus:ring-2 focus:ring-blue-500 outline-none transition-all placeholder:text-gray-600"
                placeholder="Paste your resume or upload a PDF..."
                value={resumeText}
                onChange={e => setResumeText(e.target.value)}
              />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-semibold text-gray-300">Job Description</label>
              <textarea 
                className="w-full h-32 bg-gray-900/50 border border-gray-700 rounded-2xl p-4 focus:ring-2 focus:ring-blue-500 outline-none transition-all placeholder:text-gray-600"
                placeholder="Paste the target JD here..."
                value={jdText}
                onChange={e => setJdText(e.target.value)}
              />
            </div>
          </div>

          <motion.div key={activeTab} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="bg-gray-900 border border-gray-800 rounded-3xl p-8 shadow-2xl">
            {activeTab === "upwork" && (
              <>
                <div className="flex items-center gap-4 mb-6">
                  <div className="w-12 h-12 rounded-2xl bg-green-500/20 flex items-center justify-center"><Send className="text-green-400" size={24} /></div>
                  <div>
                    <h2 className="text-2xl font-bold">Upwork Proposal Generator</h2>
                    <p className="text-gray-400">Craft a personalized proposal analyzing client metrics.</p>
                  </div>
                </div>
                <div className="flex gap-4 mb-6">
                  <div className="flex-1 space-y-2">
                    <label className="text-sm text-gray-400">Client Hiring Rate</label>
                    <input type="text" value={hiringRate} onChange={e => setHiringRate(e.target.value)} className="w-full bg-gray-950 border border-gray-700 rounded-xl p-3 outline-none" />
                  </div>
                  <div className="flex-1 space-y-2">
                    <label className="text-sm text-gray-400">Payment Verified?</label>
                    <select value={paymentVerified ? "true" : "false"} onChange={e => setPaymentVerified(e.target.value === "true")} className="w-full bg-gray-950 border border-gray-700 rounded-xl p-3 outline-none">
                      <option value="true">Yes</option>
                      <option value="false">No</option>
                    </select>
                  </div>
                </div>
                <button onClick={handleGenerateProposal} disabled={loading || !resumeText || !jdText} className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 disabled:opacity-50 text-white font-bold py-4 rounded-xl transition">
                  {loading ? "Analyzing Client & Writing Proposal..." : "Generate Premium Proposal"}
                </button>

                {/* Bookmarklet Section */}
                <div className="mt-6 p-5 bg-blue-950/40 border border-blue-900/60 rounded-2xl">
                  <h4 className="text-sm font-bold text-blue-400 mb-1 flex items-center gap-2">⚡ Upwork 1-Click Import</h4>
                  <p className="text-xs text-gray-400 mb-4 leading-relaxed">
                    Drag this button to your browser's Bookmarks bar. Open any job on Upwork, click the bookmark, and this app will open with the job details already loaded!
                  </p>
                  <a
                    href={bookmarkletHref || "#"}
                    className="inline-flex items-center gap-2 text-xs bg-blue-600 hover:bg-blue-500 text-white px-4 py-2.5 rounded-xl font-bold cursor-grab active:cursor-grabbing transition shadow-lg shadow-blue-900/30"
                    onClick={(e) => { if (!bookmarkletHref) e.preventDefault(); }}
                  >
                    🚀 Import to JobWin
                  </a>
                </div>

                {proposal && <div className="mt-8 p-6 bg-gray-950 border border-gray-800 rounded-2xl"><pre className="whitespace-pre-wrap font-sans text-gray-300">{proposal}</pre></div>}
              </>
            )}

            {activeTab === "ats" && (
              <>
                <div className="flex items-center gap-4 mb-6">
                  <div className="w-12 h-12 rounded-2xl bg-purple-500/20 flex items-center justify-center"><FileSearch className="text-purple-400" size={24} /></div>
                  <div>
                    <h2 className="text-2xl font-bold">ATS Analysis</h2>
                    <p className="text-gray-400">Compare your resume against the JD.</p>
                  </div>
                </div>
                <button onClick={handleAtsAnalysis} disabled={loading || !resumeText || !jdText} className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 disabled:opacity-50 text-white font-bold py-4 rounded-xl transition">
                  {loading ? "Analyzing..." : "Run ATS Scan"}
                </button>
                {atsResult && (
                  <div className="mt-8 space-y-6">
                    {/* Top Scores */}
                    <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                      <div className="p-4 bg-gray-950 border border-gray-800 rounded-2xl flex flex-col items-center justify-center">
                        <span className="text-sm text-gray-400 mb-1">Final Score</span>
                        <span className="text-2xl text-purple-400 font-extrabold">{atsResult.ats_score}%</span>
                      </div>
                      <div className="p-4 bg-gray-950 border border-gray-800 rounded-2xl flex flex-col items-center justify-center">
                        <span className="text-sm text-gray-400 mb-1">Keywords</span>
                        <span className="text-2xl text-blue-400 font-bold">{atsResult.keyword_score}%</span>
                      </div>
                      <div className="p-4 bg-gray-950 border border-gray-800 rounded-2xl flex flex-col items-center justify-center">
                        <span className="text-sm text-gray-400 mb-1">Semantic</span>
                        <span className="text-2xl text-pink-400 font-bold">{atsResult.semantic_score}%</span>
                      </div>
                      <div className="p-4 bg-gray-950 border border-gray-800 rounded-2xl flex flex-col items-center justify-center">
                        <span className="text-sm text-gray-400 mb-1">Experience</span>
                        <span className="text-2xl text-green-400 font-bold">{atsResult.experience_score}%</span>
                      </div>
                      <div className="p-4 bg-gray-950 border border-gray-800 rounded-2xl flex flex-col items-center justify-center">
                        <span className="text-sm text-gray-400 mb-1">Education</span>
                        <span className="text-2xl text-yellow-400 font-bold">{atsResult.education_score}%</span>
                      </div>
                    </div>
                    
                    {/* Text Analyses */}
                    <div className="space-y-4">
                      <div className="p-4 bg-gray-900 border border-gray-800 rounded-xl">
                        <h3 className="font-bold text-gray-300 mb-2">Experience Analysis</h3>
                        <p className="text-gray-400">{atsResult.experience_msg}</p>
                      </div>
                      <div className="p-4 bg-gray-900 border border-gray-800 rounded-xl">
                        <h3 className="font-bold text-gray-300 mb-2">Education Analysis</h3>
                        <p className="text-gray-400">{atsResult.education_msg}</p>
                      </div>
                      <div className="p-4 bg-gray-900 border border-gray-800 rounded-xl">
                        <h3 className="font-bold text-gray-300 mb-2">Resume Format Check</h3>
                        {atsResult.format_issues?.map((issue: string, i: number) => (
                           <p key={i} className={issue.includes('✅') ? "text-green-400 text-sm" : "text-red-400 text-sm"}>{issue}</p>
                        ))}
                      </div>
                    </div>

                    {/* Skills */}
                    <div className="grid md:grid-cols-2 gap-4">
                      <div className="p-6 bg-gray-950 border border-gray-800 rounded-2xl">
                        <h3 className="font-bold text-green-400 mb-4 flex items-center gap-2">✅ Matched Skills</h3>
                        <div className="flex flex-wrap gap-2">
                          {atsResult.matched_skills?.map((s: string) => <span key={s} className="bg-green-500/20 text-green-300 px-3 py-1 rounded-full text-sm">{s}</span>)}
                          {atsResult.matched_skills?.length === 0 && <span className="text-gray-500 text-sm">No matched skills.</span>}
                        </div>
                      </div>
                      <div className="p-6 bg-gray-950 border border-gray-800 rounded-2xl">
                        <h3 className="font-bold text-red-400 mb-4 flex items-center gap-2">❌ Missing Skills</h3>
                        <div className="flex flex-wrap gap-2">
                          {atsResult.missing_skills?.map((s: string) => <span key={s} className="bg-red-500/20 text-red-300 px-3 py-1 rounded-full text-sm">{s}</span>)}
                          {atsResult.missing_skills?.length === 0 && <span className="text-gray-500 text-sm">No missing skills!</span>}
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </>
            )}

            {activeTab === "cover" && (
              <>
                <div className="flex items-center gap-4 mb-6">
                  <div className="w-12 h-12 rounded-2xl bg-orange-500/20 flex items-center justify-center"><FileText className="text-orange-400" size={24} /></div>
                  <div><h2 className="text-2xl font-bold">Cover Letter</h2></div>
                </div>
                <button onClick={handleCoverLetter} disabled={loading || !resumeText || !jdText} className="w-full bg-orange-600 hover:bg-orange-500 disabled:opacity-50 text-white font-bold py-4 rounded-xl transition">
                  {loading ? "Writing Letter..." : "Generate Cover Letter"}
                </button>
                {coverLetter && <div className="mt-8 p-6 bg-gray-950 border border-gray-800 rounded-2xl"><pre className="whitespace-pre-wrap font-sans text-gray-300">{coverLetter}</pre></div>}
              </>
            )}

            {activeTab === "interview" && (
              <>
                <div className="flex items-center gap-4 mb-6">
                  <div className="w-12 h-12 rounded-2xl bg-teal-500/20 flex items-center justify-center"><HelpCircle className="text-teal-400" size={24} /></div>
                  <div><h2 className="text-2xl font-bold">Interview Prep</h2></div>
                </div>
                <button onClick={handleInterview} disabled={loading || !resumeText || !jdText} className="w-full bg-teal-600 hover:bg-teal-500 disabled:opacity-50 text-white font-bold py-4 rounded-xl transition">
                  {loading ? "Generating Questions..." : "Generate Interview Questions"}
                </button>
                {questions && <div className="mt-8 p-6 bg-gray-950 border border-gray-800 rounded-2xl"><pre className="whitespace-pre-wrap font-sans text-gray-300">{questions}</pre></div>}
              </>
            )}

            {activeTab === "roadmap" && (
              <>
                <div className="flex items-center gap-4 mb-6">
                  <div className="w-12 h-12 rounded-2xl bg-yellow-500/20 flex items-center justify-center"><Map className="text-yellow-400" size={24} /></div>
                  <div><h2 className="text-2xl font-bold">Learning Roadmap</h2><p className="text-gray-400">Based on missing skills from ATS Scan.</p></div>
                </div>
                <button onClick={handleRoadmap} disabled={loading || !atsResult} className="w-full bg-yellow-600 hover:bg-yellow-500 disabled:opacity-50 text-white font-bold py-4 rounded-xl transition">
                  {loading ? "Mapping Path..." : "Generate 30-Day Roadmap"}
                </button>
                {roadmap && <div className="mt-8 p-6 bg-gray-950 border border-gray-800 rounded-2xl"><pre className="whitespace-pre-wrap font-sans text-gray-300">{roadmap}</pre></div>}
              </>
            )}

            {activeTab === "tailor" && (
              <>
                <div className="flex items-center gap-4 mb-6">
                  <div className="w-12 h-12 rounded-2xl bg-blue-500/20 flex items-center justify-center"><FileSignature className="text-blue-400" size={24} /></div>
                  <div>
                    <h2 className="text-2xl font-bold">Resume Tailor (PDF)</h2>
                    <p className="text-gray-400">Automatically rewrite and format your resume to perfectly match the JD.</p>
                  </div>
                </div>
                <div className="flex gap-4">
                  <button onClick={handleTailorResume} disabled={loading || !resumeText || !jdText} className="flex-1 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 disabled:opacity-50 text-white font-bold py-4 rounded-xl transition">
                    {loading ? "Generating Tailored Resume..." : "Tailor Resume"}
                  </button>
                  {tailoredResume && (
                    <button onClick={handleDownloadPDF} className="flex-1 bg-gray-700 hover:bg-gray-600 text-white font-bold py-4 rounded-xl transition">
                      Download PDF
                    </button>
                  )}
                </div>
                {tailoredResume && (
                  <div className="mt-8 bg-white text-black p-8 rounded-xl shadow-inner max-h-[800px] overflow-y-auto">
                    <div id="resume-preview-container" dangerouslySetInnerHTML={{ __html: tailoredResume }} />
                  </div>
                )}
              </>
            )}

          </motion.div>
        </div>
      </main>
    </div>
  );
}
