import { Download, FileText } from "lucide-react";
import profile from "@/data/profile.json";

export default function Resume() {
  return (
    <section id="resume" className="py-24 max-w-6xl mx-auto px-6">
      <div className="text-center mb-16">
        <h2 className="section-title">
          My <span className="gradient-text">Resume</span>
        </h2>
        <div className="w-16 h-1 bg-gradient-to-r from-blue-500 to-teal-500 mx-auto rounded" />
      </div>

      <div className="max-w-3xl mx-auto">
        {/* Download CTA */}
        <div className="glass-card p-8 text-center mb-10">
          <FileText size={48} className="text-blue-400 mx-auto mb-4" />
          <h3 className="text-xl font-bold mb-2">Download My Full Resume</h3>
          <p className="text-slate-400 mb-6">
            PDF format — includes all experience, education, skills, and certifications.
          </p>
          <a
            href={profile.resumeUrl}
            target="_blank"
            rel="noreferrer"
            className="inline-flex items-center gap-2 px-6 py-3 bg-blue-600 hover:bg-blue-700 rounded-lg font-semibold transition-colors"
          >
            <Download size={18} /> Download Resume (PDF)
          </a>
          <p className="text-xs text-slate-600 mt-3">
            Add your resume PDF to portfolio-website/public/resume.pdf
          </p>
        </div>

        {/* Inline experience summary */}
        <div className="space-y-6">
          {profile.experience.map((exp, i) => (
            <div key={i} className="glass-card p-6">
              <div className="flex justify-between items-start mb-3">
                <div>
                  <h3 className="font-semibold text-lg">{exp.role}</h3>
                  <p className="text-teal-400">{exp.company}</p>
                </div>
                <span className="text-sm text-slate-500 shrink-0 ml-4">{exp.period}</span>
              </div>
              <ul className="space-y-1.5">
                {exp.bullets.map((b, j) => (
                  <li key={j} className="text-sm text-slate-400 flex gap-2">
                    <span className="text-blue-400 mt-1 shrink-0">▸</span>{b}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
