import { MapPin, Mail, Award } from "lucide-react";
import profile from "@/data/profile.json";

export default function About() {
  return (
    <section id="about" className="py-24 max-w-6xl mx-auto px-6">
      <div className="text-center mb-16">
        <h2 className="section-title">
          About <span className="gradient-text">Me</span>
        </h2>
        <div className="w-16 h-1 bg-gradient-to-r from-blue-500 to-teal-500 mx-auto rounded" />
      </div>

      <div className="grid md:grid-cols-2 gap-12 items-start">
        {/* Bio */}
        <div>
          <h3 className="text-2xl font-bold mb-4">
            Data Analyst &amp; Dashboard Builder
          </h3>
          <p className="text-slate-400 leading-relaxed mb-6">{profile.bio}</p>

          <div className="space-y-3">
            <div className="flex items-center gap-3 text-slate-400">
              <MapPin size={16} className="text-blue-400 shrink-0" />
              {profile.location}
            </div>
            <div className="flex items-center gap-3 text-slate-400">
              <Mail size={16} className="text-blue-400 shrink-0" />
              <a href={`mailto:${profile.email}`} className="hover:text-white transition-colors">
                {profile.email}
              </a>
            </div>
          </div>
        </div>

        {/* Experience timeline */}
        <div>
          <h3 className="text-xl font-semibold mb-6 flex items-center gap-2">
            <Award size={18} className="text-teal-400" /> Experience
          </h3>
          <div className="relative border-l-2 border-slate-700 pl-6 space-y-8">
            {profile.experience.map((exp, i) => (
              <div key={i} className="relative">
                <div className="absolute -left-[29px] w-3.5 h-3.5 rounded-full bg-blue-500 border-2 border-slate-950" />
                <div className="glass-card p-4">
                  <div className="flex justify-between items-start mb-1">
                    <h4 className="font-semibold">{exp.role}</h4>
                    <span className="text-xs text-slate-500">{exp.period}</span>
                  </div>
                  <p className="text-sm text-teal-400 mb-2">{exp.company}</p>
                  <ul className="space-y-1">
                    {exp.bullets.map((b, j) => (
                      <li key={j} className="text-sm text-slate-400 flex gap-2">
                        <span className="text-blue-400 mt-1">•</span>{b}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Education & Certifications */}
      <div className="grid md:grid-cols-2 gap-8 mt-12">
        <div className="glass-card p-6">
          <h3 className="font-semibold text-lg mb-4">Education</h3>
          {profile.education.map((edu, i) => (
            <div key={i}>
              <p className="font-medium">{edu.degree}</p>
              <p className="text-slate-400 text-sm">{edu.school} · {edu.year}</p>
            </div>
          ))}
        </div>
        <div className="glass-card p-6">
          <h3 className="font-semibold text-lg mb-4">Certifications</h3>
          <ul className="space-y-2">
            {profile.certifications.map((cert, i) => (
              <li key={i} className="flex items-center gap-2 text-sm text-slate-300">
                <span className="w-2 h-2 rounded-full bg-teal-400 shrink-0" />
                {cert}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </section>
  );
}
