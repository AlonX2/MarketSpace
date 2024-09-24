import Competitors from "./Competitors";
import NetworkChart from "./NetworkChart";

function getScoreByMatches(matches){
    var scoreSum = 0;
    for (var i = 0; i < matches.length; i++){
        const match = matches[i];
        scoreSum += match.score;
    }
    const avg = scoreSum / matches.length
    return 100 * avg;
}
function getScore(data){
    var s = 0
    const featureNames = Object.keys(data);
    for (var i = 0; i < featureNames.length; i++){
        const featureName = featureNames[i]
        const matches = data[featureName].matches;
        s += getScoreByMatches(matches);
    }
    return Math.floor(s / featureNames.length);
}
function getNeighborNum(data){
    const feature = Object.keys(data)[0];
    return data[feature]["matches"].length;
}
export default function ProductDashboard({ data }) {
    const score = getScore(data);
    const neighborNum = getNeighborNum(data);

    return (
        <div className="flex flex-col items-center justify-center">
            <div className="flex flex-row items-center justify-center my-4">
                <div className="md:mx-16 mx-4 flex flex-col items-center justify-center border-2 rounded-md border-black w-64 h-64 bg-blue-100 hover:bg-white">
                    <p className="text-6xl">{score}</p>
                    <p className="text-xl">Score</p>
                </div>
                <div className="md:mx-16 mx-4 flex flex-col items-center justify-center border-2 rounded-md border-black w-64 h-64 bg-blue-100 hover:bg-white">
                    <p className="text-6xl">{neighborNum}</p>
                    <p className="text-xl">Competitors Number</p>
                </div>
            </div>
            <Competitors featuresMatches={data}/>
            <NetworkChart className="h-64 w-128" />
        </div>
    );
}