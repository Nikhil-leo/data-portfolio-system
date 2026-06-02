import { Code2, BarChart2, Database, Cloud, Layers, Users } from "lucide-react";
import profile from "@/data/profile.json";

const SKILL_GROUPS = [
  { key: "languages",    label: "Languages",       icon: Code2 },
  { key: "visualization",label: "Visualization",   icon: BarChart2 },
  { key: "databases",    label: "Databases",       icon: Database },
  { key: "tools",        label: "Tools",           icon: Layers },
  { key: "cloud",        label: "Cloud & Platforms",icon: Cloud },
  { key: "soft",         label: "Soft Skills",     icon: Users },
] as const;

export default function Skills() {
  const skills = profile.skills as Record<string, string[]>;

  return (
    <section id="skills" className="py-24 bg-slate-900/40">
      <div className="max-w-6xl mx-auto px-6">
        <div className="text-center mb-16">
          <h2 className="section-title">
            Technical <span className="gradient-text">Skills</span>
          </h2>
          <div className="w-16 h-1 bg-gradient-to-r from-blue-500 to-teal-500 mx-auto rounded" />
        </div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {SKILL_GROUPS.map(({ key, label, icon: Icon }) => (
            <div key={key} className="glass-card p-6">
              <div className="flex items-center gap-3 mb-4">
                <div className="p-2 bg-blue-500/10 rounded-lg">
                  <Icon size={20} className="text-blue-400" />
                </div>
                <h3 className="font-semibold">{label}</h3>
              </div>
              <div className="flex flex-wrap gap-2">
                {skills[key]?.map((skill) => (
                  <span key={skill} className="pill">{skill}</span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
