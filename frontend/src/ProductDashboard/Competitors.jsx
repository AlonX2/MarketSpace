function CompetitorsOnFeature({ feature }){
    const matches = feature.matches;
    return <div className="font-sans text-lg font-medium text-slate-900">
        <p>Matches based on feature: {feature.namespace.toUpperCase()}</p>
        <ul>
            { matches.map(match => {
                return <li key={match.id}>
                    <p>Score: {match.score.toFixed(2)}</p>
                    <p>Name: {match.metadata.name}</p>
                </li>
            }) }
        </ul>
    </div>;
}

export default function Competitors({ featuresMatches }){
    return <div>
        { Object.keys(featuresMatches).map(featureName => {
            const feature = featuresMatches[featureName];
            return <CompetitorsOnFeature feature={feature}/>
        }) }
    </div>;
}