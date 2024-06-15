import NetworkChart from "./NetworkChart";

export default function ProductDashboard({ data }){
    const { score, neighbors } = data;
    const neighborNum = neighbors.length;

    return (
        <div className="flex flex-col items-center justify-center">
            <div className="flex flex-row items-center justify-center">
                <div className="md:mx-16 mx-4 flex flex-col items-center justify-center border-2 rounded-md border-black w-64 h-64 bg-blue-100 hover:bg-white">
                    <p className="text-6xl">{score}</p>
                    <p className="text-xl">Score</p>
                </div>
                <div className="md:mx-16 mx-4 flex flex-col items-center justify-center border-2 rounded-md border-black w-64 h-64 bg-blue-100 hover:bg-white">
                    <p className="text-6xl">{neighborNum}</p>
                    <p className="text-xl">Competitors Number</p>
                </div>
            </div>
            <NetworkChart className="h-64 w-128" />
        </div>
    );
}