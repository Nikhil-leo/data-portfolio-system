import { ExternalLink, BarChart2, Monitor } from "lucide-react";
import projectsData from "@/data/projects.json";

export default function Dashboards() {
  const tableauProjects = projectsData.filter((p) => p.dashboards?.tableau);
  const powerbiProjects = projectsData.filter((p) => p.dashboards?.powerbi);

  return (
    <section id="dashboards" className="py-24 bg-slate-900/40">
      <div className="max-w-6xl mx-auto px-6">
        <div className="text-center mb-16">
          <h2 className="section-title">
            Dashboard <span className="gradient-text">Gallery</span>
          </h2>
          <div className="w-16 h-1 bg-gradient-to-r from-blue-500 to-teal-500 mx-auto rounded mb-4" />
          <p className="text-slate-400 max-w-xl mx-auto">
            Interactive dashboards built in Tableau and Power BI for real-world business problems.
          </p>
        </div>

        {/* Tableau */}
        {tableauProjects.length > 0 && (
          <div className="mb-14">
            <h3 className="text-xl font-semibold mb-6 flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-orange-400" />
              Tableau Dashboards
            </h3>
            <div className="grid sm:grid-cols-2 gap-6">
              {tableauProjects.map((project) => (
                <div key={project.id} className="glass-card overflow-hidden group">
                  {/* Preview placeholder */}
                  <div className="h-48 bg-gradient-to-br from-orange-900/20 to-slate-800 flex items-center justify-center">
                    <div className="text-center">
                      <BarChart2 size={40} className="text-orange-400/40 mx-auto mb-2" />
                      <p className="text-slate-500 text-sm">Dashboard Preview</p>
                      <p className="text-slate-600 text-xs mt-1">Add screenshot to /public/projects/</p>
                    </div>
                  </div>
                  <div className="p-5">
                    <h4 className="font-semibold mb-1">{project.title}</h4>
                    <p className="text-slate-400 text-sm mb-3">{project.description}</p>
                    {project.tableauUrl &&
                      project.tableauUrl !== "https://public.tableau.com/views/your-workbook" && (
                        <a
                          href={project.tableauUrl}
                          target="_blank"
                          rel="noreferrer"
                          className="inline-flex items-center gap-1.5 text-sm text-orange-400 hover:text-orange-300 transition-colors"
                        >
                          <ExternalLink size={14} /> View on Tableau Public
                        </a>
                      )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Power BI */}
        {powerbiProjects.length > 0 && (
          <div>
            <h3 className="text-xl font-semibold mb-6 flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-yellow-400" />
              Power BI Dashboards
            </h3>
            <div className="grid sm:grid-cols-2 gap-6">
              {powerbiProjects.map((project) => (
                <div key={project.id} className="glass-card overflow-hidden group">
                  <div className="h-48 bg-gradient-to-br from-yellow-900/20 to-slate-800 flex items-center justify-center">
                    <div className="text-center">
                      <Monitor size={40} className="text-yellow-400/40 mx-auto mb-2" />
                      <p className="text-slate-500 text-sm">Dashboard Preview</p>
                      <p className="text-slate-600 text-xs mt-1">Add screenshot to /public/projects/</p>
                    </div>
                  </div>
                  <div className="p-5">
                    <h4 className="font-semibold mb-1">{project.title}</h4>
                    <p className="text-slate-400 text-sm mb-3">{project.description}</p>
                    {project.powerbiUrl &&
                      project.powerbiUrl !== "https://app.powerbi.com/view?r=your-report-id" && (
                        <a
                          href={project.powerbiUrl}
                          target="_blank"
                          rel="noreferrer"
                          className="inline-flex items-center gap-1.5 text-sm text-yellow-400 hover:text-yellow-300 transition-colors"
                        >
                          <ExternalLink size={14} /> View Power BI Report
                        </a>
                      )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </section>
  );
}
